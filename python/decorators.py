#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

from threading import Thread

def timeit(func):
    def wrapper(*args, **kwargs):
        # https://realpython.com/primer-on-python-decorators/
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        
        seconds = end-start
        print("{} seconds".format(seconds))
    return wrapper

def thread(func):
    def wrapper(*args, **kwargs):
        # https://www.saltycrane.com/blog/2008/09/simplistic-python-thread-example/
        t = Thread(target=func, args=args, kwargs=kwargs)
        t.start()
    return wrapper
