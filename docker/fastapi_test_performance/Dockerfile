FROM python:3-alpine

RUN pip3 install requests && mkdir /tests_api && mkdir /tests_api/log
ADD test_performance.py /tests_api/test_performance.py
WORKDIR /tests_api/
ENV LOG=1
CMD python3 test_performance.py
