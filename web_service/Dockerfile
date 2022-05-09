FROM python:3.8-slim-buster

WORKDIR /hipotap_web

# copy sources
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# NOTE: Need to set `FLASK_APP` envrironment variable for the app to work

CMD ["flask", "run", "--host=0.0.0.0"]
