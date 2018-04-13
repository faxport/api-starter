#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import uuid

import const
from extensions import db
from .base import BaseModel


expired_at_func = lambda: (datetime.datetime.utcnow() + datetime.timedelta(days=30)).timestamp()


class Token(BaseModel):
    __tablename__ = 'tokens'

    account_id = db.Column(db.String, db.ForeignKey('accounts.id'))
    account = db.relationship('Account')
    expired_at = db.Column(db.Float, nullable=True, default=expired_at_func)
    token = db.Column(db.String, unique=True, nullable=True, default=lambda: uuid.uuid4().hex)
