SHELL=/bin/bash -o pipefail

install: requirements.txt
	pip install -r requirements.txt

dev: requirements-dev.txt
	pip install -r requirements-dev.txt

test:
	tox
