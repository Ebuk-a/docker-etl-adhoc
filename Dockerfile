FROM python:3.11-slim-buster

RUN apt-get update -y

WORKDIR /etl

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
