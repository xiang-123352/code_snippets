# -*- coding: utf-8 -*-

"""
Setup-Routine schreiben
Import von Setup aus distutils.core

Aufrufen der Funktion setup mit kw-args
in py_modules stehen alle selbstgeschriebenen Module
"""

from distutils.core import setup

setup(
    name            = "verwirbeln",
    version         = "1.0.0",
    author          = "Gyula Orosz",
    author_email    = "Geheim@Internet.de",
    py_modules      = ["verwirbeln"]
    )