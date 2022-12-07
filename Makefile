SHELL=/bin/bash -o pipefail

install: requirements.txt
	pip install -r requirements.txt

install-dev: requirements-dev.txt
	pip install -r requirements-dev.txt

install-hooks: install-dev
	pre-commit install

.PHONY: lint
lint:
	black src
	flake8 src

test:
	tox
