# -*- coding: utf-8 -*-

import sqlite3
connection = sqlite3.connect("lagerverwaltung.db")
cursor = connection.cursor()
# Moeglichkeit an die Spaltenbezeichner zu kommen
print(cursor.description)

# Funktion schreiben
def zeilen_dict(cursor, zeile):
    ergebnis = {}
    for spaltennr, spalte in enumerate(cursor.description):
        ergebnis[spalte[0]] = zeile[spaltennr]
    return ergebnis
    
connection.row_factory = zeilen_dict
cursor.execute("SELECT * FROM kunden")
print(cursor.fetchall())

# sqlite3 liefert eine erweiterte row_factory -> sqlite3.Row
# diese ist stark optimiert -> Immer benutzen
# es sei denn die Ausgabe soll voellig abweichen -> eigene Factory
# z.B. um einen Datensatz in ein Objekt einer selbstgeschriebene
# Klasse umzuwandeln
