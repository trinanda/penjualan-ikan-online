FROM python:3.6.5-stretch

MAINTAINER Irwan Santosa

RUN apt-get update && apt-get install -y build-essential libpq-dev

# Download and install wkhtmltopdf
RUN apt-get install -y wget
RUN wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
RUN tar xvf wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
RUN mv wkhtmltox/bin/wkhtmlto* /usr/bin/

ENV INSTALL_PATH_DOCKER /web_app_docker

RUN mkdir -p $INSTALL_PATH_DOCKER

WORKDIR $INSTALL_PATH_DOCKER

COPY requirements.txt requirements_docker.txt

RUN pip install -r requirements_docker.txt

COPY . .

CMD gunicorn -b 0.0.0.0:80 --access-logfile - "web_app.app:buat_app()"
