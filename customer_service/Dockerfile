FROM python:3.8-slim-buster

WORKDIR /hipotap

# copy sources
COPY customer_service/ .
COPY hipotap_common/ ./hipotap_common/

# Update our system
RUN apt-get -y update
RUN apt-get install -y curl gnupg2 unzip

# Install Chrome.
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
# Update our system
RUN apt-get -y update
# Install Chrome
RUN apt-get -y install google-chrome-stable

RUN wget -N https://chromedriver.storage.googleapis.com/100.0.4896.20/chromedriver_linux64.zip -P ~/
RUN unzip ~/chromedriver_linux64.zip -d ~/
# Remove zip file
RUN rm ~/chromedriver_linux64.zip
# Move driver to bin location
RUN mv -f ~/chromedriver /usr/local/bin/chromedriver
# Give it rights
RUN chown root:root /usr/local/bin/chromedriver
RUN chmod 0755 /usr/local/bin/chromedriver


RUN pip3 install -r requirements.txt

CMD [ "python3", "-u", "./main.py"]
