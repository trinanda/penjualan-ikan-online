FROM python:3.6.5-stretch

MAINTAINER Irwan Santosa

RUN apt-get update && apt-get install -y build-essential libpq-dev

#RUN apt-get update && apt-get install -y libgeos-dev

#RUN pip install --upgrade google-api-python-client

#RUN pip install --upgrade python-gflags

#RUN pip install --upgrade geoalchemy2

ENV INSTALL_PATH_DOCKER /web_app_docker

RUN mkdir -p $INSTALL_PATH_DOCKER

WORKDIR $INSTALL_PATH_DOCKER

COPY requirements.txt requirements_docker.txt

RUN pip install -r requirements_docker.txt

COPY . .

CMD gunicorn -b 0.0.0.0:80 --access-logfile - "web_app.app:buat_app()"
