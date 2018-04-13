#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import *


__all__ = [
    'AccountSignupPostSchema',
    'AccountLoginPostSchema',
]


class PasswordMixin:
    password = ms.fields.Str(
        required=True,
        validate=validators.password,
        error_messages={
            'required': 'Password required',
            'null': 'Password required'
        }
    )


class EmailMixin:
    email = ms.fields.Str(
        required=True,
        validate=validators.email,
        error_messages={
            'required': 'Email required',
            'null': 'Email required'
        }
    )
    @ms.pre_load
    def append(self, data):
        if 'email' in data:
            data['email'] = data['email'].lower()
        return data



class AccountLoginPostSchema(EmailMixin, PasswordMixin, BaseSchema):
    pass

class AccountSignupPostSchema(EmailMixin, PasswordMixin, BaseSchema):
    pass
