#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from multiprocessing.dummy import Pool as ThreadPool
import subprocess

def function_proxy(*cmds):
    '''Proxy function which calls a function with parameters and kwargs'''

    # the function we really wanna call
    output = subprocess.check_output(*cmds, universal_newlines=True)

    print(output)

cmds = [("echo", "hello world"), ("ls", "-l"), "pwd"]

pool = ThreadPool(4) # number of threads

pool.map(function_proxy, cmds)
