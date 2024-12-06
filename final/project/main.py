# author:  sonnh
# email:   sonnh.tech@gmail.com
# created: 2024-12-06 19:19:28
# updated: 2024-12-07 01:16:46

from config import build_args
import pandas as pd
import pickle
from sklearn.metrics import f1_score, accuracy_score
from sklearn.preprocessing import  LabelEncoder
from xgboost import XGBClassifier

def predict(model, dataset):
    case = dataset.sample()
    X_val = dataset.drop(columns=['Label'])
    y_val = dataset['Label']

    label_encoder = LabelEncoder()
    y_val = label_encoder.fit_transform(y_val)

    # y_pred = model.predict(X_val)
    # f1 = f1_score(y_val, y_pred, average='weighted')
    # print(f"F1 score is: {f1}")

    print(case)
    model.predict(pd.DataFrame(case.drop(columns=['Label'])))

def main(main_args):
    val_dataset_ = pd.read_csv(main_args.dataset)
    model_name = main_args.model
    if model_name == 'xgboost':
        model_ = XGBClassifier()
        model_.load_model(f"models/{model_name}/model.xgb")
        predict(model_, val_dataset_)

    print('Hello World!')

if __name__ == "__main__":
    args = build_args()
    main(args)
    