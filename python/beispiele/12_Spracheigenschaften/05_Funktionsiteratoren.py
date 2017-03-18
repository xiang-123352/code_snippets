# -*- coding: utf-8 -*-


datei = open("freunde.txt")
for zeile in iter(datei.readline, ""):
	print(zeile.strip(), end=" ")