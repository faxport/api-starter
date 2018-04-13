#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import json
import os
import uuid

from flask import request
from flask_restful import Resource

import const
import decorators
import models as m
import schemas
import serializers
from . import exc


class ResourceMixin:

    def get_attr(self, key, default=None):
        return self.__dict__.get(key, default)

    @property
    def encoded_token(self):
        auth_header = request.headers.get('Authorization') or None
        if not auth_header:
            return None

        parts = auth_header.strip().split()
        if len(parts) != 2 or parts[0] != 'Bearer':
            return None
        return parts[1]

    @property
    def decoded_token(self):
        if '_decoded_token' in self.__dict__:
            return self._decoded_token

        token = self.encoded_token
        if not token:
            return None

        # find via decoded_token
        token = m.Token.query.filter(m.Token.token == token).first()
        if not token:
            return None

        # check it's expired or not
        delta = token.expired_at - datetime.datetime.utcnow().timestamp()
        if delta <= 0.0:
            token.delete()
            return None

        self._decoded_token = token
        return self._decoded_token

    @property
    def current_account(self):
        if '_current_account' in self.__dict__:
            return self._current_account

        token = self.decoded_token
        if not token:
            return None

        self._current_account = token.account
        return self._current_account

    @property
    def current_account_id(self):
        account = self.current_account
        return account.id if account else None

    @property
    def request(self):
        return request

    @property
    def global_context(self):
        ctx = {
            'current_account_id': self.current_account_id,
            'current_account': self.current_account,
        }
        return ctx

    @property
    def remote_addr(self):
        return request.headers.get('X-Real-Ip') or request.remote_addr


class BaseResource(ResourceMixin, Resource):

    def raise_exc(self, code, message, errors=None, error=None, headers=None):
        raise exc.RequestError(code=code, message=message, errors=errors,
                               error=error, headers=headers)

    def bad_request(self, message=None):
        self.raise_exc(code=400, message=message or 'Bad request')

    def access_denied(self, message=None):
        self.raise_exc(code=403, message=message or 'Access denied')

    def not_found(self, message=None):
        self.raise_exc(code=404, message=message or 'Resource not found')
