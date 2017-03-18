# -*- coding: utf-8 -*-

while True:
    zahl = int(input("Zahl eingeben: "))
    if zahl < 0:
        print("Negative Zahlen verboten")
        continue
    ergebnis = 1
    for i in range(2, zahl+1):
        ergebnis = ergebnis * i
    print("Ergebnis: ", ergebnis)