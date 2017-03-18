# -*- coding: utf-8 -*-

import sqlite3

connection = sqlite3.connect("lagerverwaltung.db")
cursor = connection.cursor()

#cursor.execute("SELECT fachnummer, komponente FROM lager")
#print(cursor.fetchall())

#cursor.execute("SELECT fachnummer, komponente FROM lager WHERE reserviert=0")
#print(cursor.fetchall())

cursor.execute("""SELECT fachnummer, komponente FROM lager
                  WHERE reserviert!=0 AND lieferant='FC'
                  """)
#print(cursor.fetchall())

cursor.execute("SELECT * FROM kunden")
#print(cursor.fetchall())

sql = """
SELECT lager.fachnummer, lager.komponente, lieferanten.name
FROM lager, lieferanten
WHERE lieferanten.telefonnummer='011235813' AND
lager.lieferant=lieferanten.kurzname"""
cursor.execute(sql)
#print(cursor.fetchall())

# Es gibt nicht nur fetchall -> fetchone
# In einer Schleife einzel Ausgaben
#cursor.execute("SELECT * FROM kunden")
#zeile = cursor.fetchone()
#while zeile:
#    print(zeile)
#    zeile = cursor.fetchone()

# BESSER IST FOLGENDE LOESUNG -> Iterator der cursor-Klasse
def alleProdukte():
    cursor.execute("SELECT * FROM lager")
    for zeile in cursor:
        print(zeile)

alleProdukte()

#cursor.execute("DELETE FROM lager WHERE seriennummer=26071987")
#connection.commit()