# -*- coding: utf-8 -*-


# getattr(object, name [,default])
class A:
	def __init__(self):
		self.X = 42

a = A()
print(getattr(a, "X"))

# Man kann auch Attribute hinzufuegen.
print(getattr(a, "Y", 404))
# Fehler kommt nur, wenn kein Defaultwert
# mit gegeben wird. (nur das Attr abgefragt wird)
print(getattr(a, "Y"))