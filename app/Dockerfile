FROM python:3.11-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache build-base &&  \
    apk add --no-cache mariadb-connector-c-dev

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

RUN apk del build-base

COPY . .