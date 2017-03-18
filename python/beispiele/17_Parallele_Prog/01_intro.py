# -*- coding: utf-8 -*-

"""
Hier reden wir ueber Threads.
Prozesse und Programme.
"""

# Arbeiten in Zyklen. Wechselnde Zuweisung der Arbeitszeit
# Zyklus = Zeitscheibe
# Wenn nicht arbeitend, dann schalfend
# Verwaltung der Zeischeiben macht das BS
# Multitasking-System (Mehrprozessorbetriebssystem)

# Leichtgewichte Threads
# Austausch zwischen Prozessen ist Intensiv und somit nicht ratsam
# Der Faden (Thread) kann sich unterteilen und somit mehrere Straenge bilden
# Jeder Prozess hat norm nur 1 Thread
# Threads teilen sich denselben Speicherbereich fuer globale Variablen
# Aenderungen innerhalb des Prozesses sofort sichtbar
# Sind fuer das BS leichter zu handhaben

# Python kann nicht verschiedene Kern ansprechen/nutzen
# Abhilfe schafft "multiprocessing"-Modul

# Es gibt 2 Module _thread und threading

# _thread ist eine einfache Variante (Jeder Thread wird als Funktion gesehen)
# threading sieht jeden Thread als Objekt

#####
# _THREADS
#####

# _tread kann einzelen Funktionen in einem separaten Thream ausfuehren
# Beispiel Approximation von Pi

def naehere_pi_an(n):
    pi_halbe = 1
    zaehler, nenner = 2.0, 1.0
    for i in range(n):
        pi_halbe *= zaehler / nenner
        if i % 2:
            zaehler += 2
        else:
            nenner += 2
    print("Annaeherung mit {} Faktoren: {:.16f}".format(n, 2*pi_halbe))

naehere_pi_an(10000000)