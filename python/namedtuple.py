#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import namedtuple
 
Point = namedtuple('Point', ['x', 'y'])    # name of the "struct" and its attributes
# Point = namedtuple('Point', 'x y')       # it would also work, and it means the same
                                           # the 2nd parameter can be a single space-delimited string
 
def main():
    p = Point(x=1, y=4)
    print(p)                # Point(x=1, y=4)
    p = Point(1, 4)
    print(p)                # Point(x=1, y=4)
    print(p.x)              # 1
    print(p[0])             # 1
    print(p == (1, 4))      # True
