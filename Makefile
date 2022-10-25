lint:
	flake8 .
	pylint .
	mypy .
	black --check --config black.toml .

format:
	black --verbose --config black.toml .
	isort **/*.py

test:
	pytest -vv .
