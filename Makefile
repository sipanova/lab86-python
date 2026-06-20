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

clean:
	@echo "---------------------------------------------------"
	@echo "Cleaning project resources"
	@echo "---------------------------------------------------"
	-@docker rm -f $(CONTAINER_NAME) 2>/dev/null || true
	-@docker rmi $(IMAGE_NAME) 2>/dev/null || true
	-@rm -f fortran_runs/*.f90
	-@rm -f fortran_runs/prime_sum_*

build-run: build run