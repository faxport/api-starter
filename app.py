#!/usr/bin/env python
# -*- coding: utf-8 -*-

import env

from flask import Flask


class Config(object):
    DEBUG = env.get_bool('DEBUG', False)
    SECRET_KEY = env.must_get('SECRET_KEY')
    SQLALCHEMY_ECHO = env.get_bool('SQLALCHEMY_ECHO', False)
    SQLALCHEMY_TRACK_MODIFICATIONS = env.get_bool('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    SQLALCHEMY_DATABASE_URI = env.must_get('DATABASE_URL')

    ERROR_404_HELP = env.get_bool('ERROR_404_HELP', False)
    BUNDLE_ERRORS = True


def create_app(app_name='api', blueprints=None):
    app = Flask(app_name)
    app.config.from_object(Config())

    _register_blueprint(app, blueprints)
    _load_extensions(app)

    return app


def _register_blueprint(app, blueprints):
    from resources import BLUEPRINTS
    blueprints = blueprints or BLUEPRINTS
    for b in blueprints:
        app.register_blueprint(b)


def _load_extensions(app):
    from extensions import db
    from extensions import migrate
    db.init_app(app)
    migrate.init_app(app, db)

    _load_extension_sentry(app)


def _load_extension_sentry(app):
    """Init sentry for logging stream.

    reference:
        - https://docs.sentry.io/clients/python/integrations/flask/
    """
    from raven.contrib.flask import Sentry
    if env.python_env not in ['production', 'demo']:
        return
    sentry = Sentry(dsn=env.must_get('SENTRY_DSN'))
    sentry.init_app(app)
