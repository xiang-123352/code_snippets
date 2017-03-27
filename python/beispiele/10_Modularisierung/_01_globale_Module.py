# -*- coding: utf-8 -*-

# Auftreilung des Quelltextes

# globale
# Interpreter ruft die Datei
# global -> systemweit
# lokal -> nur für mich (in meinem lokalen Programm)

# as ist keine Option
#import math as mathematik
#import random
#import math, random

#print(math.sin(math.pi))

from math import *
print(sin(pi))

# Funktionen und Referenzen des Moduls mit "_" werden nicht importiert
	# diese bezeichnet man als privat
	# nur innerhalb des Moduls wichtig

# zu developeTime *
# fuer produktiven Einsatz nur die wirklich
# gebrauchten Module -> kein *
from math import sin as Hallo, pi as Welt
print(Hallo(Welt))