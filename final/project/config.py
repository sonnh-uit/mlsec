# author:  sonnh
# email:   sonnh.tech@gmail.com
# created: 2024-12-07 00:40:40
# updated: 2024-12-10 16:43:00

import argparse, os
import gdown

model_uri = {
    "xgboost" : "1TnfVjojca58ac_xJs9rZzDdLNW1Y_n35",
    "decision-tree" : "1lncq8h244cwOY4JP3Y9z_x3XmOCFFQnr"
}

def download_model(model_name):
    if model_name not in ['xgboost', 'decision-tree']:
        print("Model not support!!!")
        exit(1)

    if model_name == 'xgboost':
        model_path=os.getcwd()+'/models/xgboost/model.xgb'
    else:
        model_path=os.getcwd()+'/models/decision-tree/model.pkl'

    if not os.path.isfile(model_path):
        print('Downloading model from Google Drive, please wait....')
        url = f"https://drive.google.com/uc?id={model_uri[model_name]}"
        gdown.download(url, model_path, quiet=False)
    
    return True


def build_args():
    parser = argparse.ArgumentParser(description="NT2211.CH180")
    parser.add_argument("--dataset", type=str, default="data/validate.csv", help="Path of validate data. Default is data/validate.csv")
    parser.add_argument("--model", type=str, default="decision-tree",help="Name of model want to run predict. Supporting model: `xgboost`, `decision-tree`. Default is `decision-tree`")
    args = parser.parse_args()
    return args

