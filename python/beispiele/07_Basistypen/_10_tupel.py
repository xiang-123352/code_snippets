# -*- coding: utf-8 -*-

# IMMUTABLE LIST
# Runde Klammern
tupel = (1,2,3,4,5)
print(tupel[3])

# Das ist ein int
kein_tupel = (2)
print(type(kein_tupel))

# Das ist ein Tupel
ein_tupel = (2,)
ein_tupel1 = ()
print(type(ein_tupel))
print(type(ein_tupel1))

# Tupel Packing und Tupel Unpacking
# Auto-Erstellung bei Kommanutzung
datum = 26, 7, 1967
print(datum)
print(type(datum))

# Unpacking
(tag, monat, jahr) = datum
print(tag)
print(monat)
print(jahr)

# ValueSwap
a, b = 10, 20
a, b = b, a
print(a)
print(b)

# immutable ist veraenderlich
# nur die referenzen sind unveraenderlich
# der Inhalt nicht
a = ([],)
a[0].append("Und sie dreht sich doch")
print(a)