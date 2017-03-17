#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# We will jump to this line...

# Isn't it awesome? :D

import re

f = open("zur_zeile_springen.py")

regex = "\n" # line ending

line = {1: 0}

for line_number, match in enumerate(re.finditer(regex, f.read())):
    line[line_number + 2] = match.start() + 1

# jump to line #6
f.seek(line[6])
print(f.readline())

# jump to line #4
f.seek(line[4])
print(f.readline())
