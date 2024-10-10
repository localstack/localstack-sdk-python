VENV_CMD ?= python3 -m venv
VENV_DIR ?= .venv
VENV_BIN = python3 -m venv
VENV_RUN = . $(VENV_DIR)/bin/activate
VENV_ACTIVATE = $(VENV_DIR)/bin/activate
TEST_PATH ?= .
TEST_EXEC ?= python -m
PYTEST_LOGLEVEL ?= warning
PIP_CMD ?= pip

install:			## omit dev dependencies
	uv sync --no-dev

install-dev:		## create the venv and install
	uv sync

build-spec:			## build the entire localstack api spec (openapi.yaml in the root folder)
	$(VENV_RUN); python scripts/create_spec.py

clean:         		## Clean up the virtual environment
	rm -rf $(VENV_DIR)

clean-generated:	## Cleanup generated code
	rm -rf packages/localstack-sdk-generated/localstack/

format:
	($(VENV_RUN); python -m ruff format --exclude packages .; python -m ruff check --output-format=full --exclude packages --fix .)

lint:
	($(VENV_RUN); python -m ruff check --exclude packages --output-format=full . && python -m ruff format --exclude packages --check .)

test:              		  ## Run automated tests
	($(VENV_RUN); $(TEST_EXEC) pytest --durations=10 --log-cli-level=$(PYTEST_LOGLEVEL) $(PYTEST_ARGS) $(TEST_PATH))

.PHONY: clean install install-dev
