FROM python:3.8-slim-buster

WORKDIR /hipotap

# copy sources
COPY order_service/ .
COPY hipotap_common/ ./hipotap_common/

RUN pip3 install -r requirements.txt

CMD [ "python3", "-u", "./main.py"]
