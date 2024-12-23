import os
import argparse
import logging
import pickle as pkl
from datetime import datetime
import random
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
import numpy as np
import copy
from tqdm import tqdm

# visualization packages
from sklearn.manifold import TSNE
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx

import network
import attack_func
from prep_data import get_dataset
from train import test


# create logger
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S',
                    level=logging.INFO)


def attack_by_transfer(args, model_A, model_B, attack, device, test_loader, epsilon):
    # frozen set for targeted attacks
    y_space = set(range(args.n_classes))

    # Accuracy counter
    correct = 0
    # save adversarial examples
    adv_examples = []
    adv_gt_labels = [] # ground truth labels of adversarial examples
    attack_success_labels = [] # whether the attack is successful, 0=fail, 1=success
    test_data = []
    h_adv = [] # bottleneck features of adv. examples

    # Loop over all examples in test set
    for data, target in tqdm(test_loader):

        # Send the data and label to the device
        data, target = data.to(device), target.to(device)

        # Set requires_grad attribute of tensor. Important for Attack
        data.requires_grad = True

        # Forward pass the data through the model
        output_B = model_B(data)
        init_pred = output_B.max(1, keepdim=True)[1] # get the index of the max log-probability

        # If the initial prediction is wrong, dont bother attacking, just move on
        if init_pred.item() != target.item():
            continue
        
        # add data to test_data
        test_data.append(data.detach().cpu().numpy())

        # generate adversarial example w.r.t. model A
        if args.targeted == False:
            perturbed_data, data_grad = attack.attack_batch(model_A, data, target)
        else:
            random_target = torch.LongTensor([random.choice(list(y_space.difference([target.item()])))]).to(device)
            perturbed_data, data_grad = attack.attack_batch(model_A, data, random_target)
        
        # Re-classify the perturbed image with the target model B
        h_perturbed, output = model_B(perturbed_data, return_feat=True)

        # Check for success
        final_pred = output.max(1, keepdim=True)[1] # get the index of the max log-probability

        adv_examples.append(perturbed_data.detach().cpu().numpy())
        adv_gt_labels.append(target.cpu().item())
        h_adv.append(h_perturbed.detach().cpu().numpy())
        if final_pred.item() == target.item():
            correct += 1
            attack_success_labels.append(0)
        else:
            attack_success_labels.append(1)

    # Calculate final accuracy for this epsilon
    final_acc = correct/float(len(test_loader))
    print("Epsilon: {}\tTest Accuracy = {} / {} = {}".format(epsilon, correct, len(test_loader), final_acc))

    # Return the accuracy and an adversarial example
    return final_acc, adv_examples, adv_gt_labels, attack_success_labels, test_data, h_adv


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Attack Model B with adversarial examples from model A. ')
    parser.add_argument('--dataset', type=str, 
                        choices=['mnist', 'usps', 'svhn', 'syn_digits', 
                                 'cifar10', 'stl10', ], help='dataset')
    parser.add_argument('--arch', type=str, help='network architecture')
    parser.add_argument('--ckpt_a', type=str, help='path to load model A ckpt. ')
    parser.add_argument('--ckpt_b', type=str, help='path to load model B ckpt. ')
    parser.add_argument('--attack_method', type=str, default='FGSM', help='attack method for adversarial training')
    parser.add_argument('--targeted', action='store_true', help='if set, targeted attack')
    parser.add_argument('--train_ratio', type=float, default=1.0, 
                        help='sampling ratio of training data')
    parser.add_argument('--eps', type=str, help='attack eps values, integers [0,255], split with comma')
    parser.add_argument('-g', action='store_true', help='generate and save adversarial examples')
    args = parser.parse_args()

    torch.manual_seed(1)
    random.seed(1)

    log_dir = os.path.split(args.ckpt_b)[0]
    output_path = os.path.join(log_dir, 'black-box', args.attack_method, 'targeted' if args.targeted else 'non_targeted', 
                               datetime.strftime(datetime.now(), "%d%b%y-%H%M%S"))
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    logger.info('output to {}'.format(output_path))

    args.eps = [float(v) / 255. for v in args.eps.split(',')]
    use_cuda=True

    kwargs = {'num_workers': 1, 'pin_memory': True} if use_cuda else {}
    test_loader = torch.utils.data.DataLoader(
        get_dataset(args.dataset, 'test', True, train_size=args.train_ratio, test_size=0.),
        batch_size=1, shuffle=False, **kwargs)

    # Define what device we are using
    print("CUDA Available: ",torch.cuda.is_available())
    device = torch.device("cuda" if (use_cuda and torch.cuda.is_available()) else "cpu")

    # Initialize the network
    if args.dataset == "cifar100":
        args.n_classes = 100
    elif args.dataset in ["cifar10", "stl10"]:
        args.n_classes = 9
    elif args.dataset in ["usps", "mnist", "svhn", 'syn_digits', ]:
        args.n_classes = 10
    else:
        raise ValueError('invalid dataset option: {}'.format(args.dataset))

    if args.arch == "DTN":
        model_A = network.DTN().to(device)
    elif args.arch == 'wrn':
        model_A = network.WideResNet(depth=28, num_classes=args.n_classes, widen_factor=10, dropRate=0.0).to(device)
    else:
        raise ValueError('invalid network architecture {}'.format(args.arch))
    
    model_B = copy.deepcopy(model_A).to(device)

    # Load the pretrained model
    model_A.load_state_dict(torch.load(args.ckpt_a, map_location='cpu'))
    model_B.load_state_dict(torch.load(args.ckpt_b, map_location='cpu'))

    # Set the model in evaluation mode. In this case this is for the Dropout layers
    model_A.eval()
    model_B.eval()

    transfer_test_accuracy = test(args, model_A, device, test_loader)

    accuracies = []

    # Run test for each epsilon
    for eps in args.eps:
        if args.attack_method == "FGSM":
            # TODO: magic number
            attacker = attack_func.FGSM(epsilon=eps, clip_min=-1., clip_max=1., targeted=args.targeted)
        else:
            raise NotImplementedError('attack method {} not implemented. '.format(args.attack_method))
        
        acc, adv_ex, adv_gt, attack_success_labels, test_data, h_adv = attack_by_transfer(args, model_A, model_B, attacker, device, test_loader, eps)
        attack_success_labels = np.array(attack_success_labels)
        accuracies.append(acc)
        
        # save adversarial examples
        if args.g:
            with open(os.path.join(output_path, '{}_eps{:.4f}_transfer_adv_ex.pkl'.format(args.attack_method, eps)), 'wb') as pkl_file:
                pkl.dump({"data": np.concatenate(adv_ex, axis=0), 
                          "target": np.array(adv_gt), 
                          "attack_success_flag": attack_success_labels, 
                          "features_in_model_B": np.concatenate(h_adv, axis=0)}, pkl_file)

    # summarize results
    print('eps: {}'.format(",".join([str(eps) for eps in args.eps])))
    print('accuracy: {}'.format(",".join([str(acc) for acc in accuracies])))

    with open(os.path.join(output_path, 'transfer_attack.txt'), 'w') as log_file:
        log_file.write('configs: {}\n'.format(args))
        # print('clean accuracy: {:.4f}'.format(clean_accuracy), file=log_file)
        print('eps: {}'.format(",".join([str(eps) for eps in args.eps])), file=log_file)
        print('accuracy: {}'.format(",".join([str(acc) for acc in accuracies])), file=log_file)
