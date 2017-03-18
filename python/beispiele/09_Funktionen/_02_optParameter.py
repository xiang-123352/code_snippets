# -*- coding: utf-8 -*-

# Wie in PHP DEFAULT-WERTE MIT ANGEBEN
def summe(a, b, c = 0, d = 0):
	return a + b + c + d

print(summe(1,2))
print(summe(1,2,3))
print(summe(1,2,3,4))

# SCHLUESSELWORT-PARAMETER
# Reihenfolge egal Werte an Schluessel
# Gebunden
print(summe(d=1, b=3, c=2, a=1))

# Mischen geht auch
print(summe(1, 2, c=10, d=11))