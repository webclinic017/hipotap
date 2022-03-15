FROM python:3.8-slim-buster

WORKDIR /hipotap_trip

# copy sources
COPY . .
RUN pip3 install -r requirements.txt

CMD [ "python3", "-u", "./trip_service.py"]
