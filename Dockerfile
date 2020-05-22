FROM python:3.7-slim-stretch

ENV DEBIAN_FRONTEND noninteractive
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
# Python, don't write bytecode!
ENV PYTHONDONTWRITEBYTECODE 1

# -- Install Pipenv:
RUN apt-get update && apt-get install -y build-essential git gettext-base

RUN python -m pip install -U "pip>20"
RUN python -m pip install "pipenv>=2020.4.1b1"

