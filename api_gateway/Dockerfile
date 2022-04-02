#NOTE: This dockerfile should be built from root directory of the project
FROM python:3.8-slim-buster

WORKDIR /hipotap

# copy sources
COPY api_gateway/ .
COPY hipotap_common/ ./hipotap_common/
RUN pip3 install -r requirements.txt

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]
