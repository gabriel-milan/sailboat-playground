FROM python:3.8-buster

LABEL maintainer="Gabriel Gazola Milan <gabriel.gazola@poli.ufrj.br>"

RUN mkdir -p /sailboat_playground
WORKDIR /sailboat_playground
COPY . .

RUN pip3 install --no-cache-dir -U .