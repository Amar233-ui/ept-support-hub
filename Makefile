# EPT Support Hub — developer commands.
# Windows: run from Git Bash with GNU Make (`winget install ezwinports.make`),
# or use the equivalent `docker compose` commands shown in README.md.

COMPOSE := docker compose
DB_USER ?= supporthub
DB_NAME ?= supporthub

.DEFAULT_GOAL := help
.PHONY: help setup up down restart logs ps test test-backend test-frontend test-ai \
        lint format api-types seed reset-db psql

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

setup: ## Install git hooks and local dependencies
	@test -f .env || cp .env.example .env
	cd frontend && npm install
	cd ai-service && uv sync
	npx --yes lefthook install

up: ## Start the whole dev stack (build if needed)
	@test -f .env || (cp .env.example .env && echo "Created .env from .env.example")
	$(COMPOSE) up -d --build
	@echo ""
	@echo "  Frontend : http://localhost:5173"
	@echo "  API      : http://localhost:8080/api/swagger-ui.html"
	@echo "  IA       : http://localhost:8000/docs"
	@echo "  Mailpit  : http://localhost:8025"

down: ## Stop the stack (data is kept)
	$(COMPOSE) down

restart: ## Restart one service: make restart s=backend
	$(COMPOSE) restart $(s)

logs: ## Follow logs (all, or one service: make logs s=backend)
	$(COMPOSE) logs -f --tail=100 $(s)

ps: ## Show service status
	$(COMPOSE) ps

test: test-backend test-frontend test-ai ## Run all test suites

test-backend: ## Backend unit + integration tests (Docker needed for Testcontainers)
	cd backend && ./mvnw -B verify

test-frontend: ## Frontend unit tests
	cd frontend && npm run test

test-ai: ## AI service tests
	cd ai-service && uv run pytest

lint: ## Lint all services
	cd backend && ./mvnw -B -q spotless:check
	cd frontend && npm run lint
	cd ai-service && uv run ruff check . && uv run ruff format --check .

format: ## Auto-format all services
	cd backend && ./mvnw -B -q spotless:apply
	cd frontend && npm run format
	cd ai-service && uv run ruff check --fix . && uv run ruff format .

api-types: ## Export OpenAPI from the running backend and regenerate frontend types
	curl -fsS http://localhost:8080/api/v3/api-docs | python -m json.tool > docs/openapi.json
	cd frontend && npm run api-types

seed: ## Load demo data (available from milestone M2)
	@echo "Seed data arrives with milestone M2 (scripts/seed/)."

reset-db: ## DANGER: delete the database volume and restart Postgres empty
	$(COMPOSE) rm -sf postgres
	docker volume rm -f ept-support-hub_pgdata
	$(COMPOSE) up -d postgres

psql: ## Open a psql shell in the database
	$(COMPOSE) exec postgres psql -U $(DB_USER) -d $(DB_NAME)
