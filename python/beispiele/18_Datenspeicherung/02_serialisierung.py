# -*- coding: utf-8 -*-

"""
Das Modul pickle ist genau dafuer gedacht
persistente Speicherung von Objekten & Lesen von Objekten
Serialisierung & Deserialisierung

Folgende Typen gehen:

None, False, True
numerische Typen(int, float, complex, bool)
str, bytes
sequentielle Typen (tuple, list)
Mengen(set, frozenset)
Dictionarys(solange die Daten darin serialisiert werden koennen)

Hierbei wird alles mit Klassennamen gespeichert
Der Code einer Funktion, die Definition und die Attribute
einer Klasse aber nicht

globale Funktionen
Built-In Funktionen
globale Klassen
Klasseninstanzen, deren Attribute serialisiert werden koennen
"""

# pickle hat 3 verschiedene Formate zur Speicherung von Daten
# 0 -> String besteht nur aus ASCII (a-kompatibel)
# 1 -> Binaerstring, platzsparender als 0 (a-kompatibel)
# 2 -> neues Binaerformat -> Klasseninstanz-optimiert
#      (ab Python 2.3 lesbar/nutzbar)
# 3 -> neu seit Python3 -> erst ab 3.0 nutzbar
#      unterstuetzt den neuen bytes-Typ
#      Ist Standard und wird von pickle verwendet

import pickle
"""
# pickle.dump(obj, file[, protocol])
# Speichert obj in das Dateiobjekt file (muss zum schreiben offen sein)
# protocol kann angegeben werden (siehe oben) -> 3 ist standard
# write binary
f = open("pickle-test.dat", "bw")
pickle.dump([1,2,3], f)
# file kann jedes Dateiobjekt sein, dass write-Methode implementiert
# z.B. StringIO-Instanzen

# pickle.load(file)
# Laedt die Datei ein und erkennt automatisch das Protocol
# read binary
f = open("pickle-test.dat", "rb")
res = pickle.load(f)
print(res)

"""
# pickle.dumps(obj[, protocol])
# serialisiert aus obj ein bytes-String
#pickle.dumps([1,2,3])
#print(pickle.dumps([1,2,3]))

#pickle.loads(string)
# deserialisiert aus bytes-String
#s = pickle.dumps([1,2,3,4,5])
#ds = pickle.loads(s)
#print(ds)