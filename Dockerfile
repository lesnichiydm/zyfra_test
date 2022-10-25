FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install -y gdal-bin libgdal-dev python3-gdal binutils libproj-dev

RUN  mkdir -p /root/.config/pudb
COPY ./pudb.cfg /root/.config/pudb/pudb.cfg

RUN pip install --upgrade pip
COPY ./requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

WORKDIR /app
COPY . /app
