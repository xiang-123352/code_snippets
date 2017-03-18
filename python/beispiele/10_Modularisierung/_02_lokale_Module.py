# -*- coding: utf-8 -*-

# Selbst erstellen & einbiden
# Kann nur lokal und NICHT GLOBAL genutzt werden

# import ohne .py
import mathehelfer

while True:
	zahl = int(input("Geben Sie eine Zahl ein: "))
	print("Fakultät: ", mathehelfer.fak(zahl))
	print("Kehrwert: ", mathehelfer.kehr(zahl))