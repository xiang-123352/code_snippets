#!/usr/bin/env python3

datei = open("datei.txt")
wörter = {}
wort = ""

for zeile in datei.readlines():
    wort = zeile.rstrip('\n') # Zeilenendezeichen entfernen

    if len(wort) > 0:
        wörter[wort] = 0

print(wörter)
