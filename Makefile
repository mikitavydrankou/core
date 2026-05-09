PYTHON ?= .venv/bin/python
PIP ?= $(PYTHON) -m pip

.PHONY: install-dev lint format test check precommit-install

install-dev:
	$(PIP) install -r app/requirements.txt -r requirements-dev.txt

lint:
	PYTHONPATH=app $(PYTHON) -m ruff check app tests

format:
	PYTHONPATH=app $(PYTHON) -m ruff format app tests

test:
	PYTHONPATH=app $(PYTHON) -m pytest -q

check: lint test

precommit-install:
	$(PYTHON) -m pre_commit install
