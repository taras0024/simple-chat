.PHONY: help

help: ## This help dialog.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help

LOCAL_COMPOSE_FILE ?= ./docker/compose/docker-compose.local.yml
LOCAL_DOCKER_FILE ?= ./docker/django/Dockerfile

# ----------------------------------------------------------------------------------------------------------------------
#                                           BUILD
# ----------------------------------------------------------------------------------------------------------------------
build:  ## Build docker image (Run with sudo)
	docker build -f ${LOCAL_DOCKER_FILE} -t simple-chat:dev .

# ----------------------------------------------------------------------------------------------------------------------
#                                           LOCAL
# ----------------------------------------------------------------------------------------------------------------------
up:  ## Up docker-compose
	docker compose -f ${LOCAL_COMPOSE_FILE} -p simple-chat up -d

down:  ## Down docker-compose
	docker compose -f ${LOCAL_COMPOSE_FILE} -p simple-chat down -v --remove-orphans
