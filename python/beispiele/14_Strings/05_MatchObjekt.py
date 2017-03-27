# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 13:36:54 2016

@author: gyula
"""

import re


# Match-Objekt entsteht, wenn eine match- oder search-Operation
# Uebereinstimmungen gefunden hat.
# Inhalt sind die Details der Uebereinstimmungen
m = re.match(r"(P[Yy])(th.n)", "Python")


# expand erlaubt es die uebergebenen String mit Informationen
# aus dem MS Operation zu fuellen
# dabei kann man auch Gruppen und Indezes nutzen
# m.expand(template)
print(m.expand("Hallo \g<1>-Con Fans. Hier gibt es \g<1>\g<2> satt."))


# group ermoeglicht einen komfortablen Zugriff auf die Gruppen
# Einzeln -> String
# Mehrere -> Tupel
print(m.group(1))       # 'Py'
print(m.group(1,2))     # ('Py', 'thon' )
print(m.group(0))       # gibt vollständig passenden String zurück 'Python'


# groups
# erstellt ein Tupel mit allen Teilstrings, die gepasst haben
# Tuple -> Defaultausgabe erstellen
# Geht NICHT MEHR!!! -> da das Match-Object nicht erzeugt wird, 
# wenn keine Uebereinstimmungen da sind
print(m.groups("Nix gefunden"))


# groupdict
# Gibt ein Dictionary zurueck, mit allen Gruppen als Key
# und deren Teilstrings als Werte
# Parameter default -> Wenn keine Gruppen da
c = re.compile(r"(?P<Gruppe1>P[Yy])(?P<Gruppe2>th.n)\s+(?P<Gruppe3>[Rr]ock[Zz])")
m1 = c.match("Python rockz")
print(m1.groupdict())

# Start und end geben den ersten und den letzten index des TeilStrings
# zurueck der fuer die Gruppe mit der Zahl x steht
print(m1.start(3))
print(m1.end(3))