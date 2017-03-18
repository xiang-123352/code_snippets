# -*- coding: utf-8 -*-
s = set()
fs = frozenset()
print(s)
print(fs)

s = set(("A","B","C"))
fs = frozenset([True, 47, (1,2,3)])

print(s)
print(fs)

# set kann man auch anders NUR direkt initialisieren
s = {1, 2, 3, 99, -7}
print(s)

# iteriebar
menge = {1, 100, "a", 0.5}
for elem in menge:
	print(elem)