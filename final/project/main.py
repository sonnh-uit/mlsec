# author:  sonnh
# email:   sonnh.tech@gmail.com
# created: 2024-12-06 19:19:28
# updated: 2024-12-15 21:45:59

from config import build_args, download_model
import pandas as pd
import pickle
from sklearn.metrics import f1_score, accuracy_score
from sklearn.preprocessing import  LabelEncoder
from xgboost import XGBClassifier
import json 


def boost_predict(dataset):
    download_model('xgboost')

    with open(f"models/xgboost/model_summary.json", 'r') as file:
        metrics_ = json.load(file)
    
    with open('models/xgboost/model.pkl', "rb") as file:
        model_ = pickle.load(file)

    data = dataset.drop(columns=metrics_['droped_column'][0])
    X_val = data.drop(columns=['Label'])
    label_encoder = LabelEncoder()
    y_val = label_encoder.fit_transform(data['Label'])
    y_pred = model_.predict(X_val)
    f1 = f1_score(y_val, y_pred, average='weighted')
    print(f"F1 score is: {f1}")

def DCT_predict(dataset):
    download_model('decision-tree')
    with open(f"models/decision-tree/model_summary.json", 'r') as file:
        metrics_ = json.load(file)
    with open('models/decision-tree/model.pkl', "rb") as file:
        model_ = pickle.load(file)
    data = dataset.drop(columns=metrics_['droped_column'][0])
    X_val = data.drop(columns=['Label'])
    y_val = data['Label']
    y_pred = model_.predict(X_val)
    f1 = f1_score(y_val, y_pred, average='weighted')
    print(f"F1 score is: {f1}")
    

def main(main_args):
    val_dataset_ = pd.read_csv(main_args.dataset)
    model_name = main_args.model
    if model_name == 'xgboost':
        print("Run prediction with XGBoost...")
        boost_predict(val_dataset_)
    elif model_name == 'decision-tree':
        print("Run prediction with Decision Tree...")
        DCT_predict(val_dataset_)
    else:
        print('Model not support!')
        exit(1)


if __name__ == "__main__":
    args = build_args()
    main(args)
    