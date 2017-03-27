# -*- coding: utf-8 -*-


# setattr(object, name, value)
# entspricht -> a.X = wert
class B:
	def __init__(self):
		for i in range(10):
			setattr(self, "X{}".format(i), i)

# setzt den Wert des Attributs{name}
# der Instanz{object} auf Wert value
b = B()
print(b.X3)
print(b.X8)