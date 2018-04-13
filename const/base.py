#!/usr/bin/env python
# -*- coding: utf-8 -*-

import enum
import random

import utils


class Base(enum.Enum):
    @classmethod
    def values(cls):
        return [i.value for i in list(cls)]

    @classmethod
    def choice(cls):
        return random.choice(cls.values())

    @classmethod
    def to_name(cls, value):
        return cls(value).name
