# -*- coding: utf-8 -*-

"""
SQLite unterstuetzt eine begrenzte Anzahl an Datentypen
TEXT ist unbegrenzt in der Laenge -> Guter "Container"

str.encode() -> bytes

1. alle Datentypen in str umwandeln (Adaption)
2. TEXT in DB speichern
3. TEXT aus DB Lesen
4. Urpsrungsdaten extrahieren (Konvertierung)
"""

import sqlite3

class Kreis:
    def __init__(self, mx, my, r):
        self.Mx = mx
        self.My = my
        self.R = r
    
# Adapter bauen Kreis-Obj -> str mit Werten
def kreisadapter(k):
    return "{0};{1};{2}".format(k.Mx, k.My, k.R)
    
# Umkehrfunktion str mit Werten -> Kreis-Obj
def kreiskonverter(bytestring):
    mx, my, r = bytestring.split(b";")
    return Kreis(float(mx), float(my), float(r))

# DB muss wissen, dass wir Kreise in str umwandeln wollen und speichern
# es muss registriert und an Kreis geknuepft werden
# Adapter und Konvertierer bekannt geben
sqlite3.register_adapter(Kreis, kreisadapter)
sqlite3.register_converter("KREIS", kreiskonverter)

# DB ZUgriff
conn = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)
cursor = conn.cursor()
cursor.execute("CREATE TABLE kreis_tabelle(k KREIS)")

# Kreis in DB schreiben
kreis = Kreis(1, 2.5, 3)
cursor.execute("INSERT INTO kreis_tabelle VALUES (?)", (kreis,))

# Auslesen
cursor.execute("SELECT * FROM kreis_tabelle")

# Verarbeitung
gelesener_kreis = cursor.fetchall()[0][0]
print(type(gelesener_kreis))
print(gelesener_kreis.Mx, gelesener_kreis.My, gelesener_kreis.R)

# Einschraenkungen
# sqlite3 ist an manchen Punkten eingeschraenkt
# Bei Manipulation oder Hinzufuegen von Datensaetzen
# werden lesende Zugriffe gesperrt
# Das ist im Web meist hinderlich, da mehr als 1 Nutzer Lesen
# will, wenn ein andere gerade einen Thread/Post speichert