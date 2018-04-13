#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

import marshmallow as ms
import arrow

import const
import models as m
import utils


__all__ = [
    'BaseSerializer',
    'BaseWithoutWhenSerializer',
    'EmptySerializer',
    'WhenMixin',
    'ms',
    'm',
    'const',
    'datetime',
    'arrow',
]


class WhenMixin:
    created_at = ms.fields.DateTime()
    updated_at = ms.fields.DateTime()


class BaseWithoutWhenSerializer(ms.Schema):
    id = ms.fields.String()

    @ms.post_dump
    def remove_skiped_value(self, data):
        return utils.formats.remove_none(data)


class BaseSerializer(WhenMixin, BaseWithoutWhenSerializer):
    pass


class EmptySerializer(ms.Schema):
    pass
