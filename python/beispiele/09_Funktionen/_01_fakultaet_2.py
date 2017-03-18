# -*- coding: utf-8 -*-

# Konsequente Weiterfuehrung
# Aufteilung der Augaben in Funktionen

def betrag(zahl):
	if zahl < 0:
		return -zahl
	else:
		return zahl

def fak(zahl):
	ergebnis = 1
	for i in range(2, zahl + 1):
		ergebnis *= i
	return ergebnis

#while True:
#	eingabe = int(input("Geben Sie eine Zahl ein: "))
#	print(fak(betrag(eingabe)))


print(type(fak))
p = fak
print(p(5))