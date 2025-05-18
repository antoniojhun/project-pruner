.PHONY: setup dev-setup test lint format clean pre-commit-test coverage

# Path to virtual environment activation
VENV = . venv/bin/activate &&

# Setup for users (basic installation)
setup:
	python -m venv venv
	$(VENV) pip install -e .

# Complete development environment setup
dev-setup: setup
	$(VENV) pip install -r requirements.txt
	$(VENV) pip install pre-commit
	$(VENV) pre-commit install
	npm install

# Testing
test:
	$(VENV) pytest tests/ -v

coverage:
	$(VENV) PYTHONPATH=$${PYTHONPATH}:. pytest --cov=projectpruner --cov-report=term --cov-report=html tests/
	@echo "HTML coverage report generated in htmlcov/"

pre-commit-test:
	$(VENV) pytest tests/integration_test.py::test_function -v

# Code quality
lint:
	$(VENV) ruff check src/ tests/
	$(VENV) mypy src/

format:
	$(VENV) black src/ tests/
	$(VENV) isort src/ tests/

# Cleanup
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	rm -rf htmlcov/
