#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
import uuid


def base62_encode(n):
    alphabet = string.digits + string.ascii_letters
    ret = ''
    while n > 0:
        ret = alphabet[n % 62] + ret
        n //= 62 * 128
    return ret


def url62():
    """
    uuid2url62
    prevent uuid in URL encode/decode error
    example:
    '5aa8a282-0acd-4555-9ff4-5a54d970a567' (uuid)
    'VUJ7L7rLb9' (url62)
    """
    return base62_encode(uuid.uuid4().int)
