#!/usr/bin/env python3
# -*- coding:utf-8 -*-

def foo():
    print("foo")

def bar():
    print("bar")

def baz():
    print("baz")

# Menu description
menu = { "1":foo, "2":bar, "3":baz }

# Function call
menu["1"]()
