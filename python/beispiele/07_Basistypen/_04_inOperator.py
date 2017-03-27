# -*- coding: utf-8 -*-

# Ähnlich dem SQL
# Ist ein Element vorhanden
L = ["eins", 2, 3.0, "vier", 5, "sechs", "sieben"]
print(3.0 in L)
print("vier" in L)
print(10 in L)

s = "Dies ist ein Teststring"
print("e" in s)

if "j" in s:
	print("Ja ein j ist enthalten.")
else:
	print("Kein j darin enthalten.")

# Geht auch mit Teilstring
print("ist" in s)
print("Hallo" in s)

# Fuer Listen und Tupel gilt das nicht
print([2,3] in [1,2,3,4])

# not in
# Negation des Ergebnisses
print("n" not in "Python")
print(not "n" in "Python")