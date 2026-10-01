.PHONY: help install install-dev test test-cov lint format type-check clean build docs

help:
	@echo "Medical Imaging Analyzer - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install         Install production dependencies"
	@echo "  make install-dev     Install development dependencies"
	@echo ""
	@echo "Testing:"
	@echo "  make test            Run all tests"
	@echo "  make test-cov        Run tests with coverage report"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint            Run linting checks"
	@echo "  make format          Auto-format code"
	@echo "  make type-check      Run type checking"
	@echo "  make quality         Run all quality checks"
	@echo ""
	@echo "Building:"
	@echo "  make build           Build distribution packages"
	@echo "  make clean           Clean build artifacts"
	@echo ""
	@echo "Usage:"
	@echo "  make demo            Run quick demonstration"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt
	pip install -e ".[dev]"

test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=mia --cov-report=html
	@echo "Coverage report: htmlcov/index.html"

lint:
	flake8 mia tests examples

format:
	black mia tests examples
	@echo "Code formatted with black"

type-check:
	mypy mia

quality: lint type-check
	@echo "All quality checks passed!"

clean:
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name "*.egg-info" -exec rm -r {} +
	rm -rf build/ dist/ htmlcov/ .mypy_cache/
	@echo "Cleaned up build artifacts"

build: clean
	python setup.py sdist bdist_wheel
	@echo "Built distributions in dist/"

demo:
	@echo "Running medical imaging analysis demo..."
	python -c "from mia import ImageAnalyzer; a = ImageAnalyzer(); print('Available models:'); [print(f'  - {m}') for m in a.get_available_models()]"

.DEFAULT_GOAL := help
