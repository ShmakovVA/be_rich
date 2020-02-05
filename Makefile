.PHONY: shell webpack build run test sh static migrate migrations superuser
.DEFAULT_GOAL := build

SHELL := /bin/bash

#CONTEXT ?= docker-compose
CONTEXT ?= docker-compose-gunicorn-nginx

COMPOSE = docker-compose -f ./docker/$(CONTEXT).yml -p $(PROJECT)
PROJECT ?= be_rich

stop:
	$(COMPOSE) stop

clean:
	$(COMPOSE) down -v

status:
	$(COMPOSE) ps

test:
	$(COMPOSE) run --rm my_app coverage run --source='.' manage.py test

webpack-dep:
	$(COMPOSE) run --rm my_app npm i webpack webpack-cli --save-dev
	$(COMPOSE) run --rm my_app npm i @babel/core babel-loader @babel/preset-env @babel/preset-react babel-plugin-transform-class-properties --save-dev
	$(COMPOSE) run --rm my_app npm i react react-dom prop-types react-router-dom --save-dev
	$(COMPOSE) run --rm my_app npm i weak-key --save-dev
	$(COMPOSE) run --rm my_app npm i axios --save-dev
	$(COMPOSE) run --rm my_app npm i prettier --save-dev --save-exact

webpack: static
	$(COMPOSE) run --rm my_app npm run dev

build:
	$(COMPOSE) build --pull --force-rm my_app

nginx:
	$(COMPOSE)	up nginx

shell:
	$(COMPOSE) run --rm my_app ./manage.py shell

run: webpack
	$(COMPOSE) up my_app

sh:
	$(COMPOSE) run --rm my_app ash

pgsh: rundbpg
	$(COMPOSE) run --rm postgres ash

static:
	$(COMPOSE) run --rm my_app ./manage.py collectstatic

rundbpg:
	$(COMPOSE) up -d postgres
	@(sleep 2)

dbshellpg: rundbpg
	$(COMPOSE) exec postgres psql --dbname berich --username richman

migrations: MIGRATION_TARGETS ?=
migrations:
	$(COMPOSE) run --rm -u $(shell id -u) my_app ./manage.py makemigrations $(MIGRATION_TARGETS)

migrate:
	$(COMPOSE) run --rm my_app ./manage.py migrate --noinput

superuser:
	$(COMPOSE) run --rm my_app ./manage.py createsuperuser

load-fixtures:
	$(COMPOSE) run --rm my_app ./manage.py loaddata ./backend/transactions/fixtures/fixtures.json

load-test-fixtures:
	$(COMPOSE) run --rm my_app ./manage.py loaddata ./backend/transactions/fixtures/test_fixtures.json

build-init: webpack-dep migrations migrate superuser load-fixtures webpack
	$(COMPOSE) up my_app
