# -*- coding: utf-8 -*-

import sqlite3
connection = sqlite3.connect("lagerverwaltung.db")
cursor = connection.cursor()

#print(connection.text_factory)

"""
Um str fuer Text-Spalten zu erhalten muessen wir eine eigene
tex-factory schreiben -> Parameter ist ein bytes-String
ALLES GROSS SCHREIBEN
"""
"""
def my_text_factory(value):
    return str(value, "utf-8", "ignore").upper()

# Factory umsetzen
connection.text_factory = my_text_factory
cursor = connection.cursor()
cursor.execute("SELECT * FROM kunden")
print(cursor.fetchall())
"""
"""
#sqlite3 hat eine Alternative zur text_factory
#sqlite3.OptimizedUnicode -> ist auf Geschwindigkeit optimiert
#Erkennt automatisch, ob utf-8 str oder binaer
connection1 = sqlite3.connect(":memory:")
connection1.text_factory = sqlite3.OptimizedUnicode
cursor1 = connection1.cursor()
cursor1.execute("CREATE TABLE test (spalte TEXT)")
cursor1.execute("INSERT INTO test VALUES('Hallo Welt')")
# foo utf-16 -> fuer sqlite = Binaerdatum
cursor1.execute("INSERT INTO test VALUES(?)",("foo".encode("UTF-16"),))
connection1.commit()
# Ausgabe
cursor1.execute("SELECT * FROM test")
print(cursor1.fetchall())
"""

# Connection.row_factory
# aehnliches Attribut wie text_factory
# Spaltennamen herausfinden
cursor.execute("SELECT * FROM kunden")
print(cursor.description)
#for row in rows:
#    print ("%d %s %s" % (row["kundennummer"], row["name"], row["anschrift"]))