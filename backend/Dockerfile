# get slim-buster image for python3.8
FROM python:3.8-slim-buster

#set working directory
WORKDIR /backend

#add environment variable to prevent from writing pyc files to disc and from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc postgresql \
  && apt-get clean

# install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /backend/requirements.txt
RUN pip install -r requirements.txt

COPY . /backend
