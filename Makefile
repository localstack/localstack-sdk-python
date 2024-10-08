VENV_CMD ?= python3 -m venv
VENV_DIR ?= .venv
VENV_BIN = python3 -m venv
VENV_RUN = . $(VENV_DIR)/bin/activate
VENV_ACTIVATE = $(VENV_DIR)/bin/activate
TEST_PATH ?= .
TEST_EXEC ?= python -m
PYTEST_LOGLEVEL ?= warning
PIP_CMD ?= pip

venv: $(VENV_ACTIVATE)    ## Create a new (empty) virtual environment

$(VENV_ACTIVATE): localstack-sdk-python/pyproject.toml
	test -d $(VENV_DIR) || $(VENV_BIN) $(VENV_DIR)
	$(VENV_RUN); $(PIP_CMD) install --upgrade pip
	touch $(VENV_ACTIVATE)

install: venv	#
	$(VENV_RUN); $(PIP_CMD) install -r ./localstack-sdk-generated/requirements.txt
	$(VENV_RUN); pip install -e ./localstack-sdk-generated
	$(VENV_RUN); pip install -e ./localstack-sdk-python

install-dev: install
	$(VENV_RUN); pip install -e ./localstack-sdk-python[test]

build-spec:			## build the entire localstack api spec (openapi.yaml in the root folder)
	$(VENV_RUN); python scripts/create_spec.py

clean:         	## Clean up
	rm -rf $(VENV_DIR)

clean-generated:	## Cleanup generated code
	rm -rf localstack-sdk-generated/localstack/generated

format:            		  ## Run ruff to format the whole codebase
	($(VENV_RUN); python -m ruff format .; python -m ruff check --output-format=full --exclude localstack-sdk/localstack/generated --fix .)

lint:
	($(VENV_RUN); python -m ruff check --exclude localstack-sdk/localstack/generated --output-format=full . && python -m ruff format --exclude localstack-sdk/localstack/generated --check .)

test:              		  ## Run automated tests
	($(VENV_RUN); $(TEST_EXEC) pytest --durations=10 --log-cli-level=$(PYTEST_LOGLEVEL) $(PYTEST_ARGS) $(TEST_PATH))

.PHONY: venv clean
