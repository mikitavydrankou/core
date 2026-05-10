ROOT_DIR := $(CURDIR)
GIT_ROOT := $(shell git rev-parse --show-toplevel)
PYTHON ?= $(shell if [ -x "$(ROOT_DIR)/.venv/bin/python" ]; then echo "$(ROOT_DIR)/.venv/bin/python"; elif command -v python3 >/dev/null 2>&1; then echo python3; else echo python; fi)
PIP ?= $(PYTHON) -m pip

.PHONY: install-dev lint format test check precommit-install
.PHONY: infra-up infra-down infra-logs run-api dev-start dev-stop dev

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
	cd $(GIT_ROOT) && $(PYTHON) -m pre_commit install --config core/.pre-commit-config.yaml
	cd $(GIT_ROOT) && $(PYTHON) -m pre_commit install --hook-type pre-push --config core/.pre-commit-config.yaml

infra-up:
	docker compose up -d db redis

infra-down:
	docker compose stop db redis

infra-logs:
	docker compose logs -f db redis

run-api:
	cd app && PYTHONPATH=. $(PYTHON) -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

dev-start: infra-up run-api

dev-stop: infra-down

dev: dev-start
