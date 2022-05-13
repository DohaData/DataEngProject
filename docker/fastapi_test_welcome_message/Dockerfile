FROM python:3-alpine

RUN pip3 install requests && mkdir /tests_api && mkdir /tests_api/log
ADD test_welcome_message.py /tests_api/test_welcome_message.py
WORKDIR /tests_api/
ENV LOG=1
CMD python3 test_welcome_message.py
