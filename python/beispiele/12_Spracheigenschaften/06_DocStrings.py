# -*- coding: utf-8 -*-


"""
Das ist ein DocString
Ein uber mehrere Zeilen gehender String
Dient zur Beschreibung der Klassen, Module
oder Funktionen
"""
import math
print(math.__doc__)
print()

# help erzeugt aus dem Doc eines Objektes eine
# Hilfeseite und zeigt sie im ia Modus an
print(help(math))


class MeineKlasse:
	"""Beispiel fuer DocStrings.
Diese Klasse zeigt, wie DocStrings verwendet werden.
	"""
	pass

def MeineFunktion():
	"""Diese Funktion macht nichts.
Wirklich, sie macht gar nichts.
	"""
	pass

# Ausgabe der Dokumentationen ueber
# __doc_ der Klasse oder Funktion
print(MeineKlasse.__doc__)
print(MeineFunktion.__doc__)