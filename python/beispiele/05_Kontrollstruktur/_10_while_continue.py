# -*- coding: utf-8 -*-

# Beispiel Fakultaet mit while

# while True -> IMMER WAHR
while True:
	zahl = int(input("Geben Sie eine Zahl ein: "))
	ergebnis = 1.
	while zahl > 0:
		ergebnis = ergebnis * zahl
		zahl = zahl - 1
	print("Ergebnis: ", int(ergebnis))