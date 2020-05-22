PWD ?= pwd_unknown
PROJECT_NAME = $(notdir $(PWD))
export PROJECT_NAME

.PHONY: build
build:
	docker build -t $(PROJECT_NAME)/main .