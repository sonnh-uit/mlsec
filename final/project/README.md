# Final project

In this project, I use note book to train and write some code to run model. Model experiments metrics will deliver to MLFlow. Mlflow run as container. Run and build follow by `docker-compose` file on `mlflow` folder. Before run training note book, you must run `mlflow` first.

When chose best model, I will download it from mlflow model registry. If model too large, It will be save on goolge driver. Link will note in README file

<!-- Install jupyter kernel
```
pip3 install jupyter ipykernel
python312 -m ipykernel install --user --name=mlsec --display-name "python_mlsec"
``` -->