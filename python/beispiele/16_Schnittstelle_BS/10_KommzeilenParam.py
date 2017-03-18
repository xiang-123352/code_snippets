# -*- coding: utf-8 -*-

"""
sys.argv -> Liste der Parameter bei Start -> rudimentaerer Zugang

Modul argparse -> komfortabler Umgang mit Kommandozeilenparametern
"""

import argparse as ap

# Start aus der Shell -> Name.py [Argumente]
# programm.py 1234 murmel

# Angabe von Optionen moeglich -> aehnlich Keyword Arguments
# programm.py -a gustav -b hans -c 9876 hallo welt
# 3 Optionen a, b, c
# Werte gustav, hans, 9876
# 2 Argumente -> str "hallo" und str "welt"

# parameterlos -> Flags
# programm.py -a -b 4567 tach welt
# a ist hier parameterlos -> Flag

# Bsp Taschenrechner
# Aufruf Calc.py -o {Rechenart} Zahl1 Zahl2
from argparse import ArgumentParser
parser = ArgumentParser()

# add_argument -> Erlaubte Optionen hinzufuegen
# Kurzname, Vollname, Keyword-Argument, Standardwert
parser.add_argument("-o", "--operation", dest="operation", default="plus")

# Operanden angeben
parser.add_argument("op1", type=float)
parser.add_argument("op2", type=float)

# Alles eingegeben -> auslesen der Kommandozeilenparameter & Aufbereiten
args = parser.parse_args()

# Dict mit allen moeglichen Rechenoperationen
# Schluessel dieselben, wie bei Aufruf -o
calc = {
        "plus" : lambda a, b : a + b,
        "minus" : lambda a, b : a - b,
        "mal" : lambda a , b : a * b,
        "durch" : lambda a, b : a / b
        }

# Wert auslesen, der mit -o uebergeben wurde
op = args.operation
# Wert behandeln
if op in calc:
    print("Ergebnis", calc[op](args.op1, args.op2))
else:
    parser.error("{} ist keine gültige Operation".format(op))


