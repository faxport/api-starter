#!/usr/bin/env bash

set -euo pipefail

# export env
export PYTHONPATH=.
export PYTHON_ENV=test

# erase coverage data
coverage erase

# psql
# NOTE: be careful with drop database.
psql -c "drop database if exists api_starter_test"
psql -c "drop user if exists api_starter_test"
psql -c "create user api_starter_test with password 'api_starter_test'"
psql -c "create database api_starter_test owner api_starter_test"

# upgrade db
./manage.py db upgrade

# run tests
pytest --cov-config .coveragerc --cov-append --cov-report html --cov=. tests

# coverage html report
coverage html

# open coverage report
# open coverage/index.html
