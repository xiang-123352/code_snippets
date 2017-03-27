# -*- coding: utf-8 -*-

"""
Es ist schlechter Stil und auch schlecht lesbar, wenn mehrere
Objekte in eine Datei gespeichert werden sollen.
Jedes mal das Dateiobjekt und das Protocol angeben bei dump

Abhilfe: Klasse Pickler und Unpickler

Alle Klassen erben von den beiden und somit kann man
die Seiralisierung anpassen
"""

# pickle.Pickler(file[,protocol]) -> selbe Bedeutung wie bei pickle
# Das Pickler-Obj hat eine Methode dump(obj)
# Alle Objekte werden in das Dateiobjekt geschrieben(Pickler-Instanz)

import pickle
p = pickle.Pickler(open("eine_datei.dat", "wb"), 2)
p.dump({"vorname" : "Gyula", "nachname" : "Orosz"})
p.dump([1,2,3,4,5,6,7])
p.dump("Das ist ein Test")
p.dump(("eins", "zwei", "Polizei"))

# pickle.Unpickler(file)
# Obj beitzt Methode load() -> Liest das naechste Objekt aus der Datei
u = pickle.Unpickler(open("eine_datei.dat", "rb"))
try:
    while True:
        print(u.load())
except EOFError:
    pass

# Vor Python 3.0 gab es 2 Module
# pickle und cPickle
# cPickle ist optimierte Implementation in C (schneller aber nicht
# OS-unabhaengig)
# ab 3.0 greift pickle automatisch auf eine vorhandene C-Implemantation
# zurueck, wenn da, sonst Standardimplementation