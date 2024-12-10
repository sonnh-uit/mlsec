# Final project

## Về training model
Việc training được thực hiện toàn toàn thông qua file `training.ipynb`. Quá trình training được tracking qua Mlflow, được run bằng docker trong folder mlflow.

## Về run predict model

Người dùng cần change dir tới thư mục `project`. Sau đó run file `main.py`. Example 

```bash
python3 main.py --dataset=data/train.csv --model=decision-tree
```

Trong đó 
- `--dataset`: trỏ tới đường dẫn của validate data
- `model`: tên model cần run predict