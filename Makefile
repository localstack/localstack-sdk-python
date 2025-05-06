VENV_DIR ?= .venv
VENV_RUN = . $(VENV_DIR)/bin/activate
VENV_ACTIVATE = $(VENV_DIR)/bin/activate
TEST_PATH ?= .
TEST_EXEC ?= python -m
PYTEST_LOGLEVEL ?= warning

install:			## omit dev dependencies
	uv venv
	uv sync --no-dev

install-dev:		## create the venv and install
	uv venv
	uv sync

clean:         		## Clean up the virtual environment
	rm -rf $(VENV_DIR)
	rm -rf dist/

clean-dist:
	rm -rf dist/

clean-generated:	## Cleanup generated code
	rm -rf packages/localstack-sdk-generated/localstack/

generate:			## Generate the code from the OpenAPI specs
	./bin/generate.sh

build:
	uv build --all-packages

publish: clean-dist build
	uv publish

format:
	($(VENV_RUN); python -m ruff format --exclude packages .; python -m ruff check --output-format=full --exclude packages --fix .)

lint:
	($(VENV_RUN); python -m ruff check --exclude packages --output-format=full . && python -m ruff format --exclude packages --check .)

test:              		  ## Run automated tests
	($(VENV_RUN); $(TEST_EXEC) pytest --durations=10 --log-cli-level=$(PYTEST_LOGLEVEL) $(PYTEST_ARGS) $(TEST_PATH))

.PHONY: clean install install-dev clean clean-dist clean-generated generate build publish format lint test
