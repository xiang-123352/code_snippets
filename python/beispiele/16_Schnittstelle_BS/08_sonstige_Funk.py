# -*- coding: utf-8 -*-

import sys

# exit([arg]) -> wirft eine SystemExit-Exception
# Wenn nicht gefangen, dann Programmende ohne Traceback
# arg = Ganzzahl -> ExitCode
#   0 -> alles ok
#   != 0 -> irgendein Fehler
#   Falls arg = str -> Umleitung an stderr & ExitCode = 0

# getrefcount(object) -> Anzahl der Referenzen, die auf einer
# Instanz bestehen -> Wenn = 0 -> Entsorung durch GC moeglich
# Bei unveraenderlichen Typen kann eine hohe Anzahl entstehen
# durch andauernde Neureferenzierung
triple = ('a', 'b', 'c')
print(sys.getrefcount(triple))
quarter = ('d', 'e', 'f', 'g')
print(sys.getrefcount(quarter))
triple = triple + quarter
print(sys.getrefcount(triple))

# getrecursionlimit(), setrecursionlimit()
# Lesen oder Festelegen der max. Rekusionstiefe (Standard 1000)
# bricht Endlos-Rekursion ab, bevor Speicherueberlauf

# getwindowsversion()
# Tupel (Hauptversion, Unterversion, Buildnummer, Plattform, SP)#
# Zugriff ueber Index oder Bezeichner
print(sys.getwindowsversion())

