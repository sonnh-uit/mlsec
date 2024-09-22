import torch

try:
    print(f"Torch with cuda is available:{torch.cuda.is_available()}, number of device {torch.cuda.device_count()}, device name is: {torch.cuda.get_device_name(0)}")
except:
    print("No torch with cuda available! ")