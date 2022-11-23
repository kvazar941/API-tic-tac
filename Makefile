start:
	python3 API/main.py
test:
	poetry run pytest

lint:
	poetry run flake8 API
