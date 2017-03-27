# -*- coding: utf-8 -*-

"""
Registrierung von Funktionen, die nach Beenden aufgerufen werden sollen.
    - Datensicherung
    - Netzwerkverbindungen trennen
    - Sauebern

Funktion register -> Paramter = Referenz auf Funktion
"""

#import atexit
# Beispiel
#print("Programm gestartet")
#def amEnde():
#    print("Programm beendet")
#atexit.register(amEnde)

# Endlos Eingabe
eingaben = []
def sichereEingaben(liste):
    with open("eingaben.txt", "w") as s:    
        s.writelines("\r\n".join(liste))

import atexit
atexit.register(sichereEingaben, eingaben) 

while True:
    zeile = input()
    if zeile == "exit":
        break
    eingaben += [zeile]

   
#sichereEingaben(eingaben)