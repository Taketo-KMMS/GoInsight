SRC_DIR = src
APP_DIR = $(SRC_DIR)/apps
ENTRYPOINT = $(SRC_DIR)/manage.py

PYTHON = poetry run python
DJANGO = $(PYTHON) $(ENTRYPOINT)

app-%:
	@if echo '$*' | grep -v -qE '^[a-zA-Z0-9]\w*[a-zA-Z0-9]$$'; then \
		echo "Invlida app name: $*"; \
		exit 1; \
	fi;
	mkdir -p "$(APP_DIR)/${@:app-%=%}"
	$(DJANGO) startapp ${@:app-%=%} "$(APP_DIR)/${@:app-%=%}" --template src/conf/app_template

.PHONY: run
run: migrate
	$(DJANGO) runserver_plus 0:8000

.PHONY: migrations
migrations:
	$(DJANGO) makemigrations

.PHONY: migrate
migrate:
	$(DJANGO) migrate

.PHONY: check
check: lint test

.PHONY: test
test:
	$(DJANGO) test

.PHONY: format
format:
	black .
	isort .

.PHONY: lint
lint: format
	flake8 .
	mypy .
