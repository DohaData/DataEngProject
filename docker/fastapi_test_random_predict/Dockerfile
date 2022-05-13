FROM python:3-alpine

RUN pip3 install requests && mkdir /tests_api && mkdir /tests_api/log
ADD test_random_predict.py /tests_api/test_random_predict.py
WORKDIR /tests_api/
ENV LOG=1
CMD python3 test_random_predict.py
