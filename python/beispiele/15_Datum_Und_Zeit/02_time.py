# -*- coding: utf-8 -*-

"""
- Dasselbe wie in Java
- Timestamp Start 01.01.1970 (Strat der UnixEpoche)
    1320075757.0 -> 31.10.2011 16:42:37

- 2 verschiedene Angaben: Lokalzeit & koordinierte Weltzeit

- Lokalzeit: Abhaengig vom Standort
- koordinierte Weltzeit ist die Lokalzeit auf dem Nullmeridian
    - Coordinated Universal Time (UTC)
    - Alle Lokalzeiten lassen sich relativ dazu angeben
    - UTC + 1 = Mitteleuropa
    - UTC + 2 = Deutschland

- Die tatsaechliche Lokalzeit haengt aber auch von DST ab
    - Sommer- und Winterzeit
    - Daylight Saving Time
"""

import time

# accept2dyear -> seit 3.2 deprecated

# altzone -> Verschiebung der Lokalzeit von UTC in Sekunden
    # westlich = negativ
    # oestlich = positiv
print(time.altzone//60//60)

# daylight != Sommerzeit
    # Wenn keine Sommerzeit definiert -> 0
    # Verschiebung laesst sich durch altzone ermitteln

# struct_time
    # Referenz auf struct_time Instanz
t = time.struct_time((2011, 9, 18, 18, 24, 56, 0, 0, 0))
print(t.tm_year)
print(t.tm_mon)
print(t.tm_mday)
print(t.tm_hour)
print(t.tm_min)
print(t.tm_sec)
print(t.tm_wday)
print(t.tm_yday)
print(t.tm_isdst)

# timezone -> Wie altzone, aber ohne beruecksichtigung der Sommerzeit

#tzname -> Tupel mit 2 Namen
    # 1. Name der lokalen Zeitzone
    # 2. Name der lokalen Zeitzone mit Sommerzeit
print(time.tzname)

# FUNKTIONEN

# asctime -> Wandelt ein struct_time Objekt in einen String um
print(time.asctime((1976,10,27,3,35,0,0,0,0)))
# Ohne Parameter wir die aktuelle Systemzeit zurueck gegeben
print(time.asctime())

# clock() -> gibt die akktuelle Prozessorzeit zurueck
def test_func():
    for i in range(50000000):
        i *= i
    return i
    
start = time.clock()
#print(test_func())
ende = time.clock()
print("Die Funktion lief {0:1.2f} Sekunden".format(ende - start))

# ctime -> wandelt den UNIX-Timestamp zu String um
    # bei None oder kein Parameter -> aktuelle Systemzeit

# gmtime -> wandelt Unix-Timestamp in struct_time Objekt um
    # verwendet immer UTC
    # tm_isdst immer = 0
    # bei None oder kein Parameter -> aktuelle Systemzeit
print(time.gmtime())

# localtime -> wie gmtime -> gibt aber Lokalzeit an

# mktime -> wandelt struct_time Instanz in Unix-Teimstamp der Lokalzeit um
    # ist die Umkehrfunktion von localtime
t1 = time.localtime()
t2 = time.localtime(time.mktime(t1))
print(t1 == t2)

# sleep unterbricht den Programmablauf fuer n Sekunden (float)

# strftime(format[,t]) -> wandelt struct_time Instanz in 9-Elem Tupel um
# Nutzung von Platzhaltern
print(time.strftime("%d.%m.%Y um %I:%M:%S %p Uhr"))

# strptime(string[, format]) -> Umwandlung String -> time.struct_time
zeit_string = '19.09.2011 um 00:21:17 Uhr'
print(time.strptime(zeit_string, "%d.%m.%Y um %H:%M:%S Uhr"))

# time() -> gibt UTC-Timestamp als Gleitkommazahl zurueck