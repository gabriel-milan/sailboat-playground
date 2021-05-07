FROM python:3.8-buster

LABEL maintainer="Gabriel Gazola Milan <gabriel.gazola@poli.ufrj.br>"

RUN apt-get update && apt-get install --no-install-recommends -y libgl1-mesa-dev freeglut3-dev && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /sailboat_playground
WORKDIR /sailboat_playground
COPY . .

RUN pip3 install --no-cache-dir -U .
