POETRY_VERSION = 1.2.1

# Env stuff
.PHONY: get-poetry
get-poetry:
	curl -sSL https://install.python-poetry.org | python3 - --version $(POETRY_VERSION)

.PHONY: build-env
build-env:
	python3.10 -m venv .venv
	poetry run pip install --upgrade pip
	poetry run poetry install

# Passive linters
.PHONY: black
black:
	poetry run black receipt_scanner --check

.PHONY: flake8
flake8:
	poetry run flake8 receipt_scanner

.PHONY: isort
isort:
	poetry run isort receipt_scanner --profile=black --check

.PHONY: pylint
pylint:
	poetry run pylint receipt_scanner

.PHONY: mypy
mypy:
	poetry run mypy receipt_scanner

# Aggresive linters
.PHONY: black!
black!:
	poetry run black receipt_scanner

.PHONY: isort!
isort!:
	poetry run isort receipt_scanner --profile=black

# Utilities
.PHONY: bump!
bump!:
	sh scripts/bump.sh $(filter-out $@,$(MAKECMDGOALS))

# Receive args (use like `$(filter-out $@,$(MAKECMDGOALS))`)
%:
	@:
