#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections
import datetime
import json
import re


def remove_none(obj):
    if isinstance(obj, (list, tuple, set)):
        return type(obj)(remove_none(x)
                         for x in obj if x is not None)
    elif isinstance(obj, dict):
        return type(obj)((remove_none(k), remove_none(v))
                         for k, v in obj.items()
                         if k is not None and v is not None)
    else:
        return obj


def to_snake(n):
    s = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', n)
    v = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s).lower()
    return v


def to_camecase(*args):
    n = []
    for i in args:
        if not i:
            continue
        n.extend([j.capitalize() for j in i.split('.')])
    return ''.join(n)


def to_json(data, **kwargs):
    def _json_default(obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S.%f')
        else:
            raise TypeError(obj + "cannot be serialized.")
    result = json.dumps(data, default=_json_default)
    return json.loads(result)


def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def format_safe(template, data, default=None):
    data = flatten(data or {})
    default = flatten(default or {})
    vars = re.findall(r'{(\w+)}', template)
    for i in vars:
        if i not in data:
            data[i] = default.get(i) if i in default else ''
    return template.format(**data)
