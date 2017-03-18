# -*- coding: utf-8 -*-

"""Es wird eine Datei geöffnet.
Diese wird dann versucht auszulesen
Dann wird im finally Block der
Lese-Stream geschlossen
"""
#f = open("freunde.txt", "r")
#try:
#	print(f.read())
#finally:
#	f.close()


"""Besser ist die with Variante
as Bezeichner -> nennt man auch Target
kein finally -> Deinitialisierung automatisch
"""
#with open("freunde.txt", "r") as f:
#	print(f.read())


with open("freunde.txt", "r") as f1, open("geschwister.txt", "r") as f2:
	print(f1.read())
	print(f2.read())