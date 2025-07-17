# Makefile for FastAPI HR Management Project

# Variables
ENV_FILE=.env
COMPOSE=docker-compose


# Build & Run Project
runserver:
	$(COMPOSE) up --build -d
	$(COMPOSE) exec web alembic upgrade head
	$(COMPOSE) logs -f web

# Run Test Suite
test:
	$(COMPOSE) up -d --build
	$(COMPOSE) exec web alembic upgrade head
	$(COMPOSE) exec web pytest

resetdb:
	$(COMPOSE) up -d --build
	$(COMPOSE) exec web alembic downgrade base
	$(COMPOSE) exec web alembic upgrade head


docs:
	open http://localhost:8000/docs

.PHONY: runserver test makemigration migrate resetdb bash logs stop docs
