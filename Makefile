PYTHON ?= $(shell if [ -x .venv/bin/python ]; then echo .venv/bin/python; elif command -v python3 >/dev/null 2>&1; then echo python3; else echo python; fi)
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
	$(PYTHON) -m pre_commit install --hook-type pre-push
