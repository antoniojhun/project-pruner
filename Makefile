.PHONY: setup test lint format clean pre-commit-test coverage

setup:
	python -m venv venv
	. venv/bin/activate && pip install -e .
	. venv/bin/activate && pip install -r requirements.txt
	. venv/bin/activate && pip install pre-commit
	. venv/bin/activate && pre-commit install
	npm install

test:
	. venv/bin/activate && pytest tests/ -v

coverage:
	. venv/bin/activate && PYTHONPATH=$${PYTHONPATH}:. pytest --cov=projectpruner --cov-report=term --cov-report=html tests/
	@echo "HTML coverage report generated in htmlcov/"

lint:
	. venv/bin/activate && ruff check src/ tests/
	. venv/bin/activate && mypy src/

format:
	. venv/bin/activate && black src/ tests/
	. venv/bin/activate && isort src/ tests/

pre-commit-test:
	. venv/bin/activate && pytest tests/integration_test.py::test_function -v

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	rm -rf htmlcov/
