.PHONY: help development fmt lint check dev

help:
	@echo "Usage:"
	@echo "  make setup         Set up pre-commit hooks"
	@echo "  make fmt           Format .py files"
	@echo "  make lint          Run lint checks (ruff, mypy) on .py files"
	@echo "  make check         Run pre-commit on all files (CI check)"
	@echo "  make dev           Run the development server"

setup:
	pre-commit install

fmt:
	ruff format .

lint:
	ruff check . --fix
	mypy . --ignore-missing-imports --exclude '(.venv|build|dist)'

check:
	pre-commit run --all-files --show-diff-on-failure

dev:
	uv run uvicorn api.main:app --reload
