#!/usr/bin/env python3

kleinbuchstaben = "abcdefghijklmnopqrstuvwxyz"
grossbuchstaben = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
umlaute = "äöüßÄÖÜ"
zahlen = "1234567890"
satzzeichen = ".:,;?!() "
alnum = kleinbuchstaben + grossbuchstaben + umlaute + zahlen

satz = "1, 2, 3, 4, 5, 6, 7, meine Mutter, die kocht Rüben."
wort = ""
liste = []

for buchstabe in satz:
    if buchstabe in alnum:
        wort += buchstabe
    else:
        if len(wort) > 0: # Leere Worte aus der Liste filtern
            liste.append(wort)

            wort = ""

print(liste)

