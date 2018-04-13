#!/usr/bin/env python
# -*- coding: utf-8 -*-

import env

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.dialects.postgresql import JSONB

import redis


db = SQLAlchemy(session_options={"autoflush": False})
db.JSONB = JSONB
migrate = Migrate()


_kwargs = {
    'decode_responses': True
}
r = redis.from_url(env.must_get('REDIS_URL'), **_kwargs)
