IMAGE_NAME=lab86-app
CONTAINER_NAME=lab86-container

build:
	@echo "---------------------------------------------------"
	@echo "Building Docker image: $(IMAGE_NAME)"
	@echo "---------------------------------------------------"
	@docker build -t $(IMAGE_NAME) .


run:
	@echo "---------------------------------------------------"
	@echo "Running Docker container: $(CONTAINER_NAME)"
	@echo "---------------------------------------------------"
	@docker run --rm \
		--name $(CONTAINER_NAME) \
		--env-file .env \
		$(IMAGE_NAME)

build-run: build run