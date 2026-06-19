IMAGE_NAME=lab86-app
CONTAINER_NAME=lab86-container

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run --rm --name $(CONTAINER_NAME) $(IMAGE_NAME)

build-run: build run