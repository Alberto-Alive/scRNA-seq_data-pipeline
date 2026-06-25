.PHONY: dev test lint format api docker

dev:
	pip install -e ".[dev,api]"

test:
	pytest

lint:
	ruff check .

format:
	ruff format .

api:
	uvicorn api.main:app --reload

docker:
	docker build -t scpipe .