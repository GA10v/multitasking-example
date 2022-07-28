VENV = .venv
PYTHON = $(VENV)/bin/python
PRE_COMMIT = $(VENV)/bin/pre-commit

.PHONY: install
install:
	@echo 'Installing python dependencies...'
	@poetry install
	@poetry update
	@echo 'Installing and updating pre-commit...'
	@$(PRE_COMMIT) install
	@$(PRE_COMMIT) autoupdate

.PHONY: lint
lint:
	@$(PRE_COMMIT) run --all-files

.phony: pip-to-global
pip-to-global:
	echo "[global]\nindex-url = https://pypi.org/simple" > .venv/pip.conf
