# -*- coding: utf-8 -*-

import sqlite3

# Liest die SQLite Datenbank, wenn vorhanden
# Wenn nicht, wird eine leere erstellt
connection = sqlite3.connect("lagerverwaltung.db")

# Es gibt die Möglichkeit, eine Datenbank im Arbeitsspeicher zu erzeugen,
# indem Sie statt eines Dateinamens den String ":memory:" an die
# connect-Methode übergeben:
#connection = sqlite3.connect(":memory:")

# Um mit der verbundenen Datenbank arbeiten zu können, werden sogenannte
# Cursor (dt. »Positionsanzeigen«) benötigt
# wird ueber das connection-Objekt erzeugt
cursor = connection.cursor()

# Tabelle anlegen -> Auf dem cursor -> execute()

#createLager()
def createLager():
    cursor.execute("""
    CREATE TABLE lager (
        fachnummer INTEGER,
        seriennummer INTEGER,
        komponente TEXT,
        lieferant TEXT,
        reserviert INTEGER)
    """)
    
#createLieferant()
def createLieferant():
    cursor.execute("""
    CREATE TABLE lieferanten (
        kurzname TEXT,
        name TEXT,
        telefonnummer TEXT)
    """)

#createKunde()
def createKunde():
    cursor.execute("""
    CREATE TABLE kunden (
        kundennummer INTEGER,
        name TEXT,
        anschrift TEXT)
    """)

# Daten eintragen -> Auf dem cursor -> execute()
#createFirstProduct()
def createFirstProduct():
    cursor.execute("""
    INSERT INTO lager
        VALUES(1, 26071987, 'Grafikkarte Typ 1', 'FC', 0)
    """)
# Normalerweise erst nach Eingabe bekannt
# Dann zusammensetzen des SQL-Insert-Statements mit dem String
# werte = (1, 26071987, "Grafikkarte Typ 1", "FC", 0)
# "INSERT INTO lager VALUES ({0}, {1}, '{2}', '{3}', {4})".format(*werte)
# 'INSERT INTO lager VALUES (1, 26071987, 'Grafikkarte Typ 1', 'FC', 0)'

# Bestaetigen -> auf connection-Objekt -> commit()
#connection.commit()

"""
werte = ("DR", "Danger Electronics", "666'); Hier kann Schadcode stehen")
"INSERT INTO lieferanten VALUES ('{0}', '{1}', '{2}')".format(*werte)

'INSERT INTO lager VALUES ('DR', 'Danger Electronics', '666'); Hier kann
Schadcode stehen')'

BESSER & Sicherer !!!!

werte = ("DR", "Danger Electronics", "666'); Hier kann Schadcode stehen")
sql = "INSERT INTO lieferanten VALUES (?, ?, ?)"
cursor.execute(sql, werte)

sqlite kuemmert sich um das Eintragen der richtigen Werte

NOCH VIEL BESSER

werte = {"kurz" : "DR", "name" : "Danger Electronics", "telefon" : "123456"}
sql = "INSERT INTO lieferanten VALUES (:kurz, :name, :telefon)"
cursor.execute(sql, werte)

EINEINDEUTIG
"""

# Nun koennen wir schoen unsere Tabelle fuellen
# Produkte
for row in ((1, "2607871987", "Grafikkarte Typ 1", "FC", 0),
            (2, "19870109", "Prozessor Typ 13", "LPE", 57),
            (10, "06198823", "Netzteil Typ 3", "FC", 0),
            (25, "11198703", "LED-Lüfter", "FC", 57),
            (26, "19880105", "Festplatte 128 GB", "LPE", 12)):
    cursor.execute("INSERT INTO lager VALUES (?,?,?,?,?)", row)

# anderer Weg -> mehrfach Ausfuehrung
# Lieferanten
lieferanten = (("FC", "FiboComputing Inc.", "011235813"),
               ("LPE", "LettgenPetersErnesti", "026741337"),
               ("GC", "Golden Computers", "016180339"))
#cursor.executemany("INSERT INTO lieferanten VALUES (?,?,?)", lieferanten)

# Kunden
kunden = ((12, "Heinz Elhurg","Turnhallenstr. 1, 3763 Sporthausen"),
          (57, "Markus Altbert","Kämperweg 24, 2463 Duisschloss"),
          (64, "Steve Apple","Podmacstr 2, 7467 Iwarhausen"))
#cursor.executemany("INSERT INTO kunden VALUES (?,?,?)", kunden)

#connection.commit()