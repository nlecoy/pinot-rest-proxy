develop: install-requirements setup-git

install-requirements:
	@echo "--> Installing Python dependencies (including dev only)"
	poetry install

setup-git:
	@echo "--> Installing git hooks"
	pip install pre-commit
	pre-commit install

help:
	@echo "The following targets are available:"
	@echo "  develop                 install project dependencies and git hooks"
	@echo "  install-requirements    install project dependencies"
	@echo "  setup-git               install git pre-commit hooks"

.PHONY: develop install-requirements setup-git shell help
