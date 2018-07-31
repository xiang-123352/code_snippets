#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

from threading import Thread

def timeit(func):
    def wrapper(*args, **kwargs):
        t1 = time.time()
        func(*args, **kwargs)
        t2 = time.time()
        print(">>> Time: " + str((t2 - t1)))
    return wrapper

def thread(func):
    def wrapper(*args, **kwargs):
        print(">>> Create thread...")
        t = Thread(target=func, args=args, kwargs=kwargs)
        
        print(">>> Start thread...")
        t.start()
    return wrapper
