# -*- coding: utf-8 -*-

"""
Zugriff auf geworfene Exceptions oder Arbeiten mit ihnen
"""

import sys

# exc_info()
# Zugriff auf die momentan abgefangen Exception
# Kontrollfluss innerhalb except
# Rueckgabe Tupel -> 3 Teile
#   Exception-Typ
#   geworfene Instanz des Exception-Typs
#   entsprechendes Traceback-Objekts

try:
    raise ValueError("Test")
except ValueError:
    print(sys.exc_info())
# Infos ueber Exc nur im except Zweig bekannt
# Falls auch ausserhalb -> last_type, last_value, last_traceback

# last_type, last_value, last_traceback
# Inhalte sind die Informationen der aktuell abgefangenen Exception

# tracebacklimit
# max. Tiefe der Traceback Informationen ueber die Funktionshierarchie
# standard auf 1000 gestellt
# 0 = Exception-Typ + Fehlermeldung

# Hooks sind Funktionen, die bei gewissen Aktionen des Interpreters
# aufgerufen werden -> Ueberschreiben kann die Funktionsweise
# des Interpreters aendern

# displayhook(value)
# Wird aufgerufen, wenn das Ergebnis eines Ausdrucks ausgegeben
# werden soll
# Ueberschreiben -> Aendern der Funktionalitaet
# Geht nicht bei print() -> Zeigen Interaktive Console
#def f(value):
#    print(id(value))
#
#sys.displayhook = f
#42
#97 + 32
#"Hallo Welt"
# Wiederherstellen -> sys.displayhook = sys.__displayhook__

# excepthook(type,value,traceback)
# Wird aufgerufen, wenn eine nicht abgefangen Exception auftritt
# Soll Traceback ausgeben
# Ueberschreiben mit eigenem Funktions-Objekt -> z.B. Fehler
# protokollieren oder Ausgabe veraendern
# Die 3 Parameter entsprechen denen von exc_info()
#def f(type, value, traceback):
#    print('Hahaha: "{}"'.format(value))
#sys.excepthook = f
#print("abc")
