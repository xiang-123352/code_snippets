# -*- coding: utf-8 -*-


import datetime as dati
# Es gibt 3 Konstruktoren

# datetime(year, month, day)
bday = dati.date(1987, 11, 3)
print(bday)

# datetime.date.today()
heute = dati.date.today()
print(heute)

# Neues Date Objekt wird erstellt -> aus Unix Timestamp
print(dati.date.fromtimestamp(0))

# FUNKTIONEN

print(dati.date.min)

print(dati.date.max)

# scheint nur mit neuer Zuweisung zu funktionieren
d = dati.date(2001, 7, 27)
print(d)
d = d.replace(month=12, day=12)
print(d)

d = dati.date(2011, 7, 6)
print(d.timetuple())

# weekday -> Wochentag (0 Montag - 6 Sonntag)
print(d.weekday())

# weekday -> Wochentag (1 Montag - 7 Sonntag)
print(d.isoweekday())

# isocalendar -> Tuple -> (ISO year, ISO week number, ISO weekday)
print(d.isocalendar())

# isofirmat ->gibt Datum im ISO-8601-Format zurueck (YYYY-MM-DD)
print(d.isoformat())

# ctime -> gibt einen String zurueck (24 Zeichen)
# format siehe time.strftime()
print(d.ctime())