FROM python:3.10.11
WORKDIR /mlflow
RUN pip3 install mlflow psutil pynvml
ENV BACKEND_URI sqlite:///mlflow.db
ENV MLFLOW_ENABLE_SYSTEM_METRICS_LOGGING True
EXPOSE 5000
CMD mlflow ui --backend-store-uri $BACKEND_URI --host 0.0.0.0 --port 5000