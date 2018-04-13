#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = [
    'Account',
]

import factory as f
from werkzeug.security import generate_password_hash

import const
import models
from extensions import db


class Account(f.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Account
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'commit'

    email = f.Faker('email')
    password = f.LazyAttribute(lambda o: generate_password_hash('secretpass'))
