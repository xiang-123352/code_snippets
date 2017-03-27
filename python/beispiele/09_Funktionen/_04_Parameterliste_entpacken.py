# -*- coding: utf-8 -*-

def summe(a, b, c = 0, d = 0, e = 0, f = 0):
	return a + b + c + d + e + f

t = (1, 4, 3, 7, 9, 2)
#print(summe(t[0], t[1], t[2], t[3], t[4], t[5]))

# Kuerzer
#print(summe(*t))

# Geht auch beio Dictionary
d = {"a" : 7, "b" : 3, "c" : 4}
#print(summe(**d))

# Kombiniertes Entpacken
print(summe(1, *(2,3), **{"d":4}))