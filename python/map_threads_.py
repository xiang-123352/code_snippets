#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from multiprocessing.dummy import Pool as ThreadPool
import subprocess

def function_proxy(*cmds):
    foo = subprocess.check_output(*cmds, universal_newlines=True)

    print(foo)

def map_thread():
    cmds = [("echo", "hello world"), ("ls", "-l"), "pwd"]

    pool = ThreadPool(4) # number of threads
    pool.map(function_proxy, cmds)

map_thread()
