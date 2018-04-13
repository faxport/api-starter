#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import *


__all__ = [
    'AccountSerializer',
    'AccountMinSerializer',
    'AccountWithTokenSerializer',
]


class AccountMinSerializer(BaseSerializer):
    class Meta:
        additional = (
            'email',
        )


class AccountSerializer(AccountMinSerializer):

    class Meta:
        additional = AccountMinSerializer.Meta.additional + (
        
        )


class AccountWithTokenSerializer(AccountSerializer):
    access_token = ms.fields.String()
