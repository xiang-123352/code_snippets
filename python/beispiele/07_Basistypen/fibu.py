#!/usr/bin/python
# -*- coding: utf-8 -*-

c = 0
lst = [0, 1]
wert = int(input('Bitte Endwert eingeben: '))
while len(lst) < wert:

    # lst.append(lst[c + 1] + lst[c])

    lst.insert(len(lst), lst[c + 1] + lst[c])
    c += 1

print lst
