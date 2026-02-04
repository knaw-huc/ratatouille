all: help

check-dependencies:
	@echo "--- Checking global prerequisites ---">&2
	@command -v python3 || (echo "Missing dependency: python3" && false)
	@command -v poetry || (echo "Missing dependency: poetry" && false)

.PHONY: install
install: check-dependencies
	@echo "--- Installing package locally ---">&2
	poetry lock && poetry install

.PHONY: test
test:
	poetry run pytest -q

.PHONY: run
run:
	@echo "--- Running index merger ---">&2
	poetry run merge-indices

.PHONY: help
help:
	@echo "make tools for ratatouille"
	@echo "Please use \`make <target>', where <target> is one of:"
	@echo
	@echo "  install               - to install ratatouille locally using poetry"
	@echo "  merge-indices         - to run the index merger"
