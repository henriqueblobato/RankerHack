include .env
export

DOCKER_IMAGE_NAME = ranker_hack

.PHONY: all build run

all: build run

build:
	docker build -t $(DOCKER_IMAGE_NAME) .

run:
	docker run -it $(DOCKER_IMAGE_NAME)

clean:
	docker stop $$(docker ps -a -q) || true
	docker rm $$(docker ps -a -q) || true
	docker rmi $$(docker images -q) || true

help:
	@echo "Available targets:"
	@echo "  make build         - Build the Docker image"
	@echo "  make run           - Run the app inside a Docker container"
	@echo "  make clean         - Stop and remove all Docker containers and images"
	@echo "  make help          - Display this help message"

