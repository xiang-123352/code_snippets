# -*- coding: utf-8 -*-

# Weitere Parameter
# werden in ein Tupel gespeichert
def funktion(a, b, *mehr):
	print("Feste Parameter: ", a, b)
	print("Weitere Parameter: ", mehr)

#print(funktion(1,2))
#print(funktion(1, 2, "Hallo", 42, [1, 2, 3, 4]))

# Fuer unbekannte Anzahl Parameter
def summe(*param):
	s = 0
	for p in param:
		s += p
	return s

#print(summe(1,2,3,4,5))
#print(summe(1,2,3,4,5,6,7,8,9,10,11,12))

# Keyword Arguments
# Weitere Parameter -> in Dictionary
def funktion1(a, b, **weitere):
	print("Feste Parameter: ", a, b)
	print("Weitere Parameter: ", weitere)

#print(funktion1(1,2))
#print(funktion1(1,2, Juergen = "Meister", Gyula = "Padawan"))

# Mischen der Arten
# *positional ist ein Tuple
# **keyword ist ein Dictionary
def funktion2(*positional, **keyword):
	print("Positional: ", positional)
	print("Keyword: ", keyword)

#print(funktion2(1, 2, 3, 4, hallo="welt", key="word"))

# Reine Schluesselwort-Parameter
#def f(a, b, *c, d, e):
#	print(a, b, c, d, e)

# Fehler -> nach Pos-Param nur noch KW-Param
#print(f(1,2,3,4,5))

# Behoben
def f1(a, b, *c, d=4, e=5):
	print(a, b, c, d, e)

print(f1(1, 2, 3, 4, 5))

def f2(a, b, *args, d, e, **kwargs):
	print(a, b, args, d, e, kwargs)

#print(f2(1, 2, 3, 4, 5, 6))
#print(f2(1, 2, 3, d=4, e=5, f=6))

# Platzhalter
def f3(a, b, *, c, d):
	print(a, b, c, d)
#print(f3(1,2,3,4))
print(f3(1,2,c=3,d=4))