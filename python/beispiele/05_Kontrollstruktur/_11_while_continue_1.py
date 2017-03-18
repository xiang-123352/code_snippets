# -*- coding: utf-8 -*-

# Beispiel Fakultaet mit while

# while True -> IMMER WAHR
while True:
	zahl = int(input("Geben Sie eine Zahl ein: "))
	if zahl < 0:
		print("Negative Zahlen verboten")
		continue
	ergebnis = 1.
	while zahl > 0:
		ergebnis = ergebnis * zahl
		zahl = zahl - 1
	print("Ergebnis: ", ergebnis)