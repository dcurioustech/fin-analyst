# Financial Analysis Bot - Makefile

.PHONY: help install test test-verbose test-coverage test-unit test-integration clean lint

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	pip install -r requirements.txt

test:  ## Run all tests with pytest
	python -m pytest tests/

test-verbose:  ## Run tests with verbose output
	python -m pytest tests/ -v

test-coverage:  ## Run tests with coverage report
	python -m pytest tests/ --cov=. --cov-report=html --cov-report=term-missing

test-unit:  ## Run only unit tests
	python -m pytest -m "unit or not integration"

test-integration:  ## Run integration tests
	python -m pytest integration_tests/ -v

test-specific:  ## Run specific test file (usage: make test-specific FILE=tests/test_utils.py)
	python -m pytest $(FILE)

test-pattern:  ## Run tests matching pattern (usage: make test-pattern PATTERN=test_format)
	python -m pytest -k "$(PATTERN)"

clean:  ## Clean up generated files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .pytest_cache/

lint:  ## Run linting (if you have flake8 or similar installed)
	@echo "Add your linting commands here (flake8, black, etc.)"

test-all:  ## Run both unit and integration tests
	python -m pytest tests/ integration_tests/ -v

test-smoke:  ## Run smoke tests only
	python integration_tests/test_suite_simple.py

# GitHub Actions related commands
ci-test:  ## Run tests as they would run in CI
	python -m pytest tests/ integration_tests/ -v --tb=short --durations=10

ci-lint:  ## Run linting as it would run in CI
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

ci-security:  ## Run security checks as they would run in CI
	bandit -r . -ll
	safety check

docker-build:  ## Build Docker image
	docker build -t fin-analyst:latest .

docker-run:  ## Run Docker container locally
	docker run -p 8080:8080 --env-file .env fin-analyst:latest

docker-test:  ## Test Docker container
	docker build -t fin-analyst:test .
	docker run --rm fin-analyst:test python -m pytest tests/ -v