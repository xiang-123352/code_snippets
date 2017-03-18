# -*- coding: utf-8 -*-

"""
Objekte des Typs time dienen dazu, Tageszeiten anhand von Stunde, Minute,
Sekunde und auch Mikrosekunde zu verwalten.
In dem Attribut tzinfo können time-Instanzen Informationen zur lokalen Zeitzone
speichern und ihre Werte damit an die Lokalzeit anpassen.
"""

# Konstruktor Paramter = 4 Ganzzahlen
# 0 < hour < 24
# 0 < minute < 60
# 0 < second < 60
# 0 < microsecond < 1000000
# letzter ist eine Instanz von datetime.tztime

import datetime as dt

t = dt.time(14,30,45,0)
print(t)

# geht nur mit neuer Zuweisung
nt = t.replace(minute=40, second=55, microsecond= 100)
print(nt)

# isoformat -> siehe DT

#strftime(format) -> siehe DT

# datetime.datetime -> Ein Typ zum speichern aller Informationen
    # Datum und Uhrzeit

# Konstruktoren
bescherung = dt.datetime(2016,12,24,17,00)
print(bescherung)

# GENAU JETZT
print(dt.datetime.today())

# now -> siehe today()
print(dt.datetime.now())

# utcnow -> Same as now fuer koordinierte Weltzeit
print(dt.datetime.utcnow())

# fromtimestamp -> erzeugt aus Timestamp eine Instanz von datetime
import time
t = time.time()
print(dt.datetime.fromtimestamp(t))

#utcfromtimestamp -> siehe oben fuer koordinierte Weltzeit
print(dt.datetime.utcfromtimestamp(t))

# combine(date, time) -> erzeugt einen Hybriden
# date = datetime-date Objekt && time = datetime.time Objekt

#strptime(date_string, format) -> Bei gueltigem String gibt er ein
# entsprechendes datetime Objekt zurueck
# format-> siehr strftime

# RECHNEN MIT DATUM

# 100 Tage mit date
print(dt.date(1987, 11, 3) - dt.date(1987, 7, 26))

# 10 Stunden mit datetime
d1 = dt.datetime(2012,2,15,17,0,0)
d2 = dt.datetime(2012,2,15,7,0,0)
print(d1 - d2)

# +100 Tage mit timedelta -> Zeitspannen
print(dt.date(1987, 7, 26) + dt.timedelta(100))

# VERGLEICHEN
print(dt.date(1987, 7, 26) < dt.date(1987, 11, 3))

# TIME DELTA
d1 = dt.datetime(2012, 1, 9, 12, 0, 0)
d2 = dt.datetime(2012, 2, 10, 20, 15, 0)
delta1 = d2 - d1
# 32 Tage 8 Stunden 15 Minuten (Zukunft)
print(delta1)

delta2 = d1 - d2
# -33 Tage +15 Stunden +45 Minuten (Vergangenheit)
print(delta2)

# Beide gleich (1pos und 1neg -> Summe = 0)
print(delta1+ delta2)

# Rechnung bei neg:
# 32 Tage 8 Stunden und 15 Minuten sind in neg
# -33 Tage
# +15 Stunden
# +45 Minuten

# Konstruktor
# timedelta([days[,seconds[,microseconds[,milliseconds[,minutes[,hours[,weeks]]]]]]])

# intern arbeitet er nur mit Tage, Sekunden und Microsekunden
# Eine Millisekunde wird zu 1000 Mikrosekunden.
# Eine Minute wird zu 60 Sekunden.
# Eine Stunde wird zu 3600 Sekunden.
# Eine Woche wird zu 7 Tagen.

# Die Attribute days, seconds und microseconds werden als ganze Zahlen
# gespeichert.Dabei gelten folgende Einschränkungen:
# -999999999  days < 999999999
# 0  seconds < 3600*24
# 0  microseconds < 1000000
# Es ist zu beachten, dass nur das days-Attribut ein negatives Vorzeichen haben
# kann, das angibt, ob die timedelta-Instanz in Richtung Zukunft oder
# Vergangenheit zeigt.