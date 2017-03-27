# -*- coding: utf-8 -*-

"""
Das Tabellenformat: CSV (Comma Separated Values)

weit verbreitetes Import- und Exportformat fuer
Tabellenkalkulation oder EmailClients
Werte innerhalb der Datei durch Trennzeichen getrennt
z.B. Komma

Beispiel:

vorname,nachname,geburtsdatum,wohnort,haarfarbe
Heinrich,Huhn,19.07.1980,Berlin,Braun
Rudolf,Geier,19.09.1990,Dortmund,Braun
Haken,Habicht,14.04.1959,Hamburg,Dunkelblond
Edith,Falke,13.09.1987,Köln,Schwarz
Rüdiger,Amsel,25.03.1988,München,Hellrot

Die erste Zeile -> Spaltenbezeichner
Danach die Datensaetze

Es gibt keinen festen Standard im Bezug der Separierung

CSV-Modul implementiert reader und writer Klassen
Diese kapseln den Lese- und Schreibzugriff auf die CSV-Dateien

Eine Liste mit allen definierten Dialekten unter
csv.list_dialects()
['excel-tab', 'excel', 'unix']
"""

import csv

#print(csv.list_dialects())


# Aus CSV lesen -> reader-Objekte

# csv.reader(csvfile[,dialect][,**fmtparam])
# csvfile -> Referenz auf fuer Lesezugriff geoeffnetes Dateiobjekt
# dialect -> in welchem Format wurde die Datei geschrieben
# Standard ist dabei 'excel' und 'comma'
# **fmtparam -> keyword-Parameter (Kein Umweg ueber dialect-Klasse)
#reader = csv.reader(open("personen.csv"), delimiter=";")

# reader Instanzen implementieren das Iterator-Protokol
# Spaltenwerte werden immer als String zurueckgegeben
#reader = csv.reader(open("personen.csv"))
#for row in reader:
#    print(row)

# Dict-Reader -> erzeugt Dictionary
#reader = csv.DictReader(open("personen.csv"))
#for pers in reader:
#    print(pers)



# In CSV schreiben -> writer-Objekte
# csv.writer(csvfile[,dialect][,**ftmparam])
# writerow und writerows werden implementiert
# alles wird als String gespeichert
#writer = csv.writer(open("autos.csv", "w"))
#writer.writerow(["marke", "model", "leistung_in_ps"])
"""
daten= (
["Volvo", "P245", "130"], ["Ford", "Focus", "90"],
["Mercedes", "CLK", "250"], ["Audi", "A6", "350"],
)
"""
#writer.writerows(daten)

# Dictwriter -> analog zu DictReader
"""
writer = csv.DictWriter(open("autos1.csv", "w"),
                        ["marke", "modell", "leistung_in_ps"])
writer.writerow({"marke" : "marke", "modell" : "modell",
                 "leistung_in_ps" : "leistung_in_ps"})
daten = ({"marke" : "Volvo", "modell" : "P245", "leistung_in_ps" : "130"},
         {"marke" : "Ford", "modell" : "Focus", "leistung_in_ps" : "90"},
         {"marke" : "Mercedes", "modell" : "CLK", "leistung_in_ps" : "250"},
         {"marke" : "Audi", "modell" : "A6", "leistung_in_ps" : "350"})
writer.writerows(daten)
"""

"""
reader = csv.reader(open("autos1.csv"))
for row in reader:
    print(row)

reader = csv.DictReader(open("autos1.csv"))
for pers in reader:
    print(pers)
"""

# Dialect-Objekte -> sollen CSV-Dateien beschreiben
# werden normalerweise nicht erzeugt -> csv.register_dialect()
# dann auch in Liste csv.get_dialects()
# csv.register_dialect(name[,dialect][,**fmtparam])
# name muss ein String sein, der den neuen Dialekt identifiziert
# dialect kann ein schon bestehendes Objekt sein, dass dann mit dem
# Name verknuepft wird
# Bepsiel: csv.register_dialect("mein_dialekt", delimiter="\t",
#                                quoting=csv.QUOTE.ALL)

# TEMPFILE FOLGT, ABER UNWICHTIG -> SPAETER VIELLEICHT