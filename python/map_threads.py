#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from multiprocessing.dummy import Pool as ThreadPool
import subprocess

cmds = [("pluma", "new.txt"), ("pluma", "old.txt"), "xterm"]

pool = ThreadPool(4) # number of threads

pool.map(subprocess.call, cmds)
