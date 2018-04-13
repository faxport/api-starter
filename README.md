API Starter

#### Introduction

This is a simple starter for HTTP JSON API.

Main Stack:
- Web Framework: Flask
- ORM: SQLAlchemy
- Database: PostgreSQL
- Others:
  - alembic for database migration
  - marshmallow for json serialization, deserialization and validation
  - py.test for testing

#### Getting started

- dotenv sample: see [.env.sample](.env.sample)
- new dotenv for multiple environments, e.g.: `.env.development`
- export environments: `export PYTHONPATH=.`
- run app: `./manage.py runserver`

#### Testing

- run tests: `./run_tests.sh`

#### Reference
- [Welcome | Flask (A Python Microframework)](http://flask.pocoo.org/)
- [SQLAlchemy - The Database Toolkit for Python](https://www.sqlalchemy.org/)
- [marshmallow: simplified object serialization — marshmallow 3.0.0b8 documentation](https://marshmallow.readthedocs.io/en/latest/)
- [Welcome to Alembic’s documentation! — Alembic 0.9.10 documentation](http://alembic.zzzcomputing.com/en/latest/)
