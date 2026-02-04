.PHONY: all
all: help

.PHONY: clean-dependencies
clean-dependencies:
	-rm -rf env

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
	@echo "--- Merging indices ---">&2
	. env/bin/activate && merge-indices

help:
	@echo "make tools for ratatouille"
	@echo "Please use \`make <target>', where <target> is one of:"
	@echo "  install-dependencies  - to install the necessary dependencies for ratatouiile"
	@echo
	@echo "  merge-indices         - to run the index merger"
	@echo
	@echo "  clean-dependencies    - clean local dependencies (python env)"
