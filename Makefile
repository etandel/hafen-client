.PHONY: test

MODULES ?= hafen_client tests

RUNNER ?= poetry run

all: black-format check-all

check-all: linters test

linters: black-check mypy flake8

black-format:
	$(RUNNER) black $(MODULES)

black-check:
	$(RUNNER) black --check $(MODULES)

flake8:
	$(RUNNER) flake8 $(MODULES)

mypy:
	$(RUNNER) mypy --ignore-missing-imports --strict-optional $(MODULES)

PYTESTARGS ?= -vv --tb=native --cov=hafen_client

test:
	$(RUNNER) pytest $(PYTESTARGS)

publish:
	poetry publish --build
