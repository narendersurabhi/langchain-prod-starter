.PHONY: setup lint format type test run

setup:
	uv sync --all-extras

lint:
	ruff check .

format:
	ruff format .

type:
	mypy src

test:
	pytest

run:
	uvicorn lc_app.api.main:app --host 0.0.0.0 --port 8000
