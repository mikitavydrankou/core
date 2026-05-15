ROOT_DIR := $(CURDIR)
GIT_ROOT := $(shell git rev-parse --show-toplevel)
PYTHON ?= $(shell if [ -x "$(ROOT_DIR)/.venv/bin/python" ]; then echo "$(ROOT_DIR)/.venv/bin/python"; elif command -v python3 >/dev/null 2>&1; then echo python3; else echo python; fi)
PIP ?= $(PYTHON) -m pip
DB_URL ?= postgresql+asyncpg://postgres:secret@localhost:5432/taxi
ALEMBIC ?= DATABASE_URL=$(DB_URL) $(PYTHON) -m alembic
REV ?= -1

.PHONY: install-dev lint format test check
.PHONY: infra-up infra-down infra-logs run-api dev-start dev-stop dev
.PHONY: db-revision db-upgrade db-downgrade db-current db-history

install-dev:
	$(PIP) install -r app/requirements.txt -r requirements-dev.txt

lint:
	PYTHONPATH=app $(PYTHON) -m ruff check app tests

format:
	PYTHONPATH=app $(PYTHON) -m ruff format app tests

test:
	PYTHONPATH=app $(PYTHON) -m pytest -q

check: lint test

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

#make db-revision msg="add_driver_states"
db-revision:
	$(ALEMBIC) revision --autogenerate -m "$(msg)"

db-upgrade:
	$(ALEMBIC) upgrade head

#make db-downgrade REV=fcce49a3b5bb
db-downgrade:
	$(ALEMBIC) downgrade $(REV)

db-current:
	$(ALEMBIC) current

db-history:
	$(ALEMBIC) history
