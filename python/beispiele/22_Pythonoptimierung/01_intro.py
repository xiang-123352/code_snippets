# -*- coding: utf-8 -*-

"""
Einfachheit und Effizienz sind das A und O
Kontrapunkte -> effizient ist meist nicht einfach

Solange nicht laufzeit-kritisch, Balance aus Eleganz und Effizients

Sonst nur Effizient

Auch Speicherplatz-Optimierung ist ein Augenerk

Hoechtse Laufzeitgewinn durch Optimierung der Algorithmik selbst

Optimierung nur da, wo unbedingt noetig
"""

# ***************
# Optimize-Option
# ***************

# Beeinflussung des Laufzeitverhaltens durch Kommandozeilenparameter -0
# Interpreter -> ByteCode-Optimierung
# Asserts werden nicht ins Kompilat aufgenommen
    # if __debug__:
    #   tu_was()
# optimierte Dateien haben die Endung *.pyo
# -00 : Extra optimiert -> DocStrings fallen raus, help nicht mehr moeglich

# *********************
# Mutable vs- Immutable
# *********************
 
# Veraenderbarkeit der Datentypen haben eine performancetechnische Relevanz
# Beispiel Tuple -> Zahlen 0-49999
# 1. Anlegen
# 2. Schleife -> Anhaengen der Zahlen an das Tuple (jedes Mal neue Instanz)

import time

"""
start = time.clock()
tup = ()
for i in range(50000):
    tup += (i,)
ende = time.clock()
#print(tup)
print("Die Funktion lief {0:1.2f} Sekunden".format(ende - start))
"""

# Alternative -> Liste (veraenderbar)
# Keine neue Instanz -> Kann je nach Groesse bis zu 90% schneller sein
"""
start = time.clock()
lst = []
for i in range(5000000):
    lst += [i]
ende = time.clock()
#print(lst)
print("Die Funktion lief {0:1.2f} Sekunden".format(ende - start))
"""

# *********
# Schleifen
# *********

# Listen sind gut, aber nicht optimiert
# Comprehensions koennen bis zu 60% schneller sein
# Beispiel als Comprehension
# sind schneller als analoge Zaehlschleifen

lst = []
start = time.clock()
lst += [i for i in range(5000000)]
ende = time.clock()
#print(lst)
print("Die Funktion lief {0:1.2f} Sekunden".format(ende - start))
