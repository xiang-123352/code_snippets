#!/usr/bin/env python3
# -*- coding: utf-8 -*-

f = open("file.txt")
words = {}
word = ""

for line in f.readlines():
    word = line.rstrip('\n') # Remove line ending

    if len(word) > 0:
        words[word] = 0

print(words)
