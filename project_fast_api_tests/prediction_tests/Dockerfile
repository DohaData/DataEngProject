FROM debian:latest

RUN apt-get update && apt-get install -y curl && apt-get install python3-pip -y && pip3 install requests==2.27.1

ADD prediction_check.py /tests/prediction_check.py

WORKDIR /tests/

CMD python3 prediction_check.py

