.PHONY: all
all: help

install-dependencies:
	@echo "--- Checking global prerequisites ---">&2
	@command -v python3 || (echo "Missing dependency: python3" && false)
	@echo "--- Installing local dependencies ---">&2
	make env

env: requirements.txt
	@echo "--- Setting up virtual environment ---">&2
	python3 -m venv env && . env/bin/activate && pip install --upgrade pip && pip install -r requirements.txt
	touch $@

.PHONY: run
run:
	merge-indices

.PHONY: install
install:
	pip install -e .

help:
	@echo "make tools for ratatouille"
	@echo "Please use \`make <target>', where <target> is one of:"
	@echo "  install        - to install this package locally in the currently selected virtual env"
	@echo "  merge-indices  - to run the index merger"
