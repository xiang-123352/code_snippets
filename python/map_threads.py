#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from multiprocessing.dummy import Pool as ThreadPool
import subprocess

def map_thread():
    cmds = [("echo", "hello world"), ("ls", "-l"), "pwd"]

    pool = ThreadPool(4) # number of threads
    pool.map(subprocess.check_output, cmds)
