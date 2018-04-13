#!/usr/bin/env python
# -*- coding: utf-8 -*-


def routes():
    from app import create_app
    app = create_app()
    result = []
    for rule in app.url_map.iter_rules():
        route = {
            'url': rule.rule,
            'endpoint': rule.endpoint,
            'methods': ','.join(rule.methods),
            'rule': rule,
        }
        result.append(route)
    return result
