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

# _ ist ein unausgesprochenes Gesetz
# NICHT ANFASSEN -> private

a = A()
print(a.getX())
a.setX(300)
print(a.getX())
a.setX(-20)
print(a.getX())