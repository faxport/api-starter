#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import random

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

import env
import const
from extensions import db
from .base import BaseModel
from .token import Token
import utils


class Account(BaseModel):
    __tablename__ = 'accounts'

    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def soft_delete(self):
        self.deleted_at = datetime.datetime.utcnow()
        self.save()

        Token.delete_by(account_id=self.id)

    def set_password(self, password):
        self.password = generate_password_hash(password)
        self.save()

        Token.delete_by(account_id=self.id)

    def check_password(self, password):
        return check_password_hash(self.password, password)
