# -*- coding: utf-8 -*-


#class A:
#	def __del__(self):
#		print("Ich bin der Destruktor")

# Erst nachdem auch die letzte Referenz auf
# die Instanz geloescht wurde, wird der
# Destruktor aufgerufen
#a = A()
#b = a
#del a
#del b


#class Potenz:
#	def __init__(self, exponent):
#		self.Exponent = exponent
#
#	def __call__(self, basis):
#		return basis ** self.Exponent
#
#dreier_potenz = Potenz(3)
#print(dreier_potenz(2))
#print(dreier_potenz(5))


# __slot__ Hinzufuegen von Attributen
# zur Laufzeit
#class B:
#	pass
#
#b = B()
#b.X = 10
#print(b.X)


# Anzahl der hinzufuegbaren Attribute einschraenken
# NIcht vererbar
class B:
	__slots__ = ("X", "Y")
	def __init__(self):
		self.X = 1
		self.Y = 2

b = B()
print(b.X)
print(b.Y)
#print(b.Z)