PWD ?= pwd_unknown
PROJECT_NAME = $(notdir $(PWD))
export PROJECT_NAME

PYTHON_VERSION=3.8
PIPENV_VERSION=2020.6.2
IMAGE_NAME=tolgaeren/pipenv-in-a-container:${PYTHON_VERSION}-${PIPENV_VERSION}
.PHONY: build
build:
	PYTHON_VERSION=${PYTHON_VERSION} PIPENV_VERSION=${PIPENV_VERSION} envsubst < Dockerfile.template > Dockerfile
	docker build -t ${IMAGE_NAME} .
	docker push ${IMAGE_NAME}