FROM debian:latest

RUN apt-get update && apt-get install -y curl && apt-get install python3-pip -y && pip3 install requests==2.27.1

ADD test_performance_check.py /tests/test_performance_check.py

WORKDIR /tests/

CMD python3 test_performance_check.py
