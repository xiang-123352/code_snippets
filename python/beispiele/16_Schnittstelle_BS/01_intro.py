# -*- coding: utf-8 -*-

"""
Python ist OS-uebergreifend, um Problemen mit OS-bezogenen
Funktionen aus dem Weg zu gehen.
Es wurde eine Schnittstelle geschaffen, die einheitlichen
Zugriff auf OS-Funktionen bietet.

Das Modul os implementiert diese Schnittstelle
"""

# Zugriff auf mehrere Klassen von Operationen
#   - Zugriff auf eigenen(Python) Prozess und andere Prozesse
#   - Zugriff auf das Dateisystem
#   - Informationen ueber das BS

#       - os.path bietet nuetzliche Operationen zu Manipulation
#         und Verarbeiteung von Pfadnamen

#   - os hat eine eigene Exception Klasse -> os.error
#   - innerhalb des Moduls nuztbar -> alternativ OSError

# Seit Python 3.0 wird streng zwischen Text und Daten durch die Datentypen
# str und bytes unterschieden
# Kurz: str rein – str raus; bytes rein – bytes raus.


import os

# Konstante environ -> enthaelt ein Dict (Umgebungsvariablen)
# Aenderungen moeglich, aber VORSICHT !!!!!
print(os.environ['HOMEDRIVE'] + os.environ['HOMEPATH'] + "\r\n")

# getpid() -> Python-Prozess, der das laufende Programm ausfuehrt
# Nur unter Unix und Windows moeglich
print(os.getpid())

# system(cmd) -> Kommandos des BS ausfuehren wie in einer Shell
# Beispiel -> neuer Ordner "test_ordner" uber mkdir
# 0 heisst Erfolg
# Ausgaben lass sich nicht ohne Weiteres ermitteln
print(os.system("mkdir test_ordner"))

# BESSER popen(smd[,mode[,buffsize]])
# damit werden x Befehle auf einer Komm-Zeile des BS ausgefuehrt
# Rueckgabe ist ein dateiaehnliches Objekt -> Zugriff auf Ausgabe
# mode -> "r" || "w"
# Beispiel dir fuer C:\

ausgabe = os.popen("dir /B C:\\")
dateien = [zeile.strip() for zeile in ausgabe]
print(dateien)