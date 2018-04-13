#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cProfile
import pstats
import functools
import time


def perf_profile(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        s = time.time()
        result = func(*args, **kwargs)
        pr.disable()
        ps = pstats.Stats(pr)
        ps.sort_stats('cumulative').print_stats(10)
        print('perf_time: elaspsed {0:.6f}s'.format(time.time() - s))
        return result

    return wrapper
