# author:  sonnh
# email:   sonnh.tech@gmail.com
# created: 2024-12-07 00:40:40
# updated: 2024-12-07 11:09:28

import argparse

def build_args():
    parser = argparse.ArgumentParser(description="NT2211.CH180")
    parser.add_argument("--dataset", type=str, default="data/validate.csv")
    parser.add_argument("--model", type=str, default="xgboost",help="`xgboost`")
    args = parser.parse_args()
    return args