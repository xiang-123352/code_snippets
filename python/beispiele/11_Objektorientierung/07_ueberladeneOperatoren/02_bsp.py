# -*- coding: utf-8 -*-


class Laenge:
	Umrechnung = {
		"m":1, "dm":0.1, "cm":0.01,
		"mm":0.001, "km":1000,
		"ft":0.3048,	# Fuss
		"in": 0.0254,	# Zoll
		"mi":1609344	# Meile
		}


	def __init__(self, zahlenwert, einheit):
		self.Zahlenwert = zahlenwert
		self.Einheit = einheit


	def __str__(self):
		return "{0:f}{1}".format(self.Zahlenwert, self.Einheit)


	def __add__(self,other):
		z = self.Zahlenwert * Laenge.Umrechnung[self.Einheit]
		z += other.Zahlenwert * Laenge.Umrechnung[other.Einheit]
		z /= Laenge.Umrechnung[self.Einheit]
		return Laenge(z, self.Einheit)


	def __sub__(self, other):
		z = self.Zahlenwert * Laenge.Umrechnung[self.Einheit]
		z -= other.Zahlenwert * Laenge.Umrechnung[other.Einheit]
		z /= Laenge.Umrechnung[self.Einheit]
		return Laenge(z, self.Einheit)

# Dictionary mit Umrechnungen
# __add__ und __sub__ sind ueberladen
# erst Umrechnung der Operanden auf Meter, dann Rest
a1 = Laenge(5, "cm")
a2 = Laenge(3, "dm")
# Der 1. Operand bestimmt die Einheit
print(a1 + a2)
print(a2 + a1)

