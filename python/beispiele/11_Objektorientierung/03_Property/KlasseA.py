# -*- coding: utf-8 -*-


class A:
	
	def __init__(self):
		self._X = 100

	def getX(self):
		return self._X

	def setX(self, wert):
		if wert < 0:
			return
		self._X = wert

	X = property(getX, setX)

# Der Zugriff auf X wird mit Property
# auf die getX und setX Methode gesetzt
# Sie werden automatisch implizit genutzt

a = A()
print(a.X)
a.X = 300
print(a.X)
a.X = -20
print(a.X)