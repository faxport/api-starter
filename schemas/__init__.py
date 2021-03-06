#!/usr/bin/env python
# -*- coding: utf-8 -*-

import utils

from .base import *

# account
from .account import *


def get_by(pattern, *args):
    """Get schema by pattern."""
    if not pattern.endswith('Schema'):
        pattern += 'Schema'
    value = utils.formats.to_camecase(*args)
    name = pattern.format(value)
    return globals().get(name)
