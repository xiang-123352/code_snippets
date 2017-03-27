# -*- coding: utf-8 -*-

# ****************
# Funktionsaufrufe
# ****************

# Manchmal ist es sinnvoller Funktionsaufrufe zu "inlinen"
# Verkettung von Funktionen und Objekten in einer Zeile
"""
def f(s):
    return s.upper()
ergebnis = f("Hallo Welt")
# ist 30% langsamer als
ergebnis = "Hallo Welt".upper()
"""

# ***
#  C
# ***

# C ist hardwarenaeher, darum schneller.
# Bei laufzeitkritischen Algorithmen sollte man das Programm in C
# schreiben und danach implementieren.
# Built-In Funktionen sind so geschrieben, darum immer vorzuziehen

# ******
# Lookup
# ******

# Bei Zugriff auf Funktion ueber Modul, muss ein Lookup durchgefuehrt werden
# bei Java -> static -> Math.round()
# Bei Referenzen auf die Funktion ist das nicht noetig
# Beispiel Wurzel ziehen aus 0 bis 100

import math
import time

"""
# indirekte Nutzung ueber Modul math
start = time.clock()
wurzeln = [math.sqrt(i) for i in range(1,10000001)]
ende = time.clock()
#print(wurzeln)
print("Die Funktion lief {0:1.2f} Sekunden".format(ende - start))
"""
"""
# 20% effizienter -> Referenzieren
start = time.clock()
s = math.sqrt
wurzeln = [s(i) for i in range(1,10000001)]
ende = time.clock()
#print(wurzeln)
print("Die Funktion lief {0:1.2f} Sekunden".format(ende - start))
"""

# **********
# Exceptions
# **********

"""
# Beispiel Zugriff auf eine Liste, mit wechselndem Index
# Unbekannt, ob Index vorhanden oder nicht
def f(liste, i):
    if i in liste:
        return liste[i]
    else:
        return 0
"""

"""
# besser ist ein direkter Zugriff auf liste[i]
# und bei Exception -> 0
# bis zu 35% schneller ab ca. 100 Eintraege
# Davor ist die erste Methode schneller
# Wie Bubble-Sort
def f(liste, i):
    try:
        return liste[i]
    except IndexError:
        return 0
"""

# *****************
# Keyword Arguments
# *****************
"""
# Sind ineffizienter als reiner Argumentenaufruf
def f(a,b,c,d):
    return "{} {} {} {}".format(a,b,c,d)
print(f("Hallo", "du", "schöne", "Welt"))
# 18% schneller als
print(f(a="Hallo", b="du", c="schöne", d="Welt"))
"""