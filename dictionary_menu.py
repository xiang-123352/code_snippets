#!/usr/bin/env python3

def foo():
    print("foo")

def bar():
    print("bar")

def baz():
    print("baz")

# Menübeschreibung
menue = { "1":foo, "2":bar, "3":baz }

# Funktionsaufruf
menue["1"]()
