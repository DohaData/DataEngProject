FROM debian:latest

ADD requirements.txt fraud_detection_app.py fraud_detection_models.py fraud_lgb.pkl fraud_rfc.pkl /app/

RUN apt-get update && apt-get install python3-pip -y && pip3 install -r app/requirements.txt

WORKDIR /app

CMD ["uvicorn", "fraud_detection_app:api", "--host", "0.0.0.0", "--port", "8000"]
