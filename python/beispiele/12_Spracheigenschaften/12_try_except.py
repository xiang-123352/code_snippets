# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 11:20:11 2017

@author: gunny
"""

import os

file = "woerterbuch.dict"
wb = {}

'''
if not os.path.exists(file):
    f = open(file, "w")
    f.close()
else:
    pass
'''

try:
    f = open(file)
    for line in f:
        line = line.strip()
        elems = line.split(" ")
        wb[elems[0]] = elems[1]
    f.close()
except (IOError, TypeError) as e:
    print(e)

try:
    eingabe_1 = int(input("Bitte geben Sie eine Zahl ein: "))
    eingabe_2 = int(input("Bitte geben Sie eine weitere Zahl ein: "))
    print("Summe: ", eingabe_1 + eingabe_2)
    print("Produkt: ", eingabe_1 * eingabe_2)
    print("Diff: ", eingabe_1 - eingabe_2)
    print("Div: ", eingabe_1 / eingabe_2)
except (ZeroDivisionError, ValueError) as e:
    print(e)
else:
    print("Du hast alles richtig gemacht")
finally:
    print("Ich bin immer der letzte")