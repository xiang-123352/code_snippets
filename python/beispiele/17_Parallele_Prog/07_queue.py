# -*- coding: utf-8 -*-

"""
Arbeiten mit Warteschlangen.
Konstruktor -> Parameter = Ganzzahl (Anzahl Auftraege)
bei Anzahl <= 0 (unbegrenzt)
3 Methoden:
    put:        stellt Auftraege in die Queue
    get:        liefert die nächste Aufgabe
                (blockiert auch Threads bis Verfuegbarkeit neuer Auftraege)
    task:done:  Benachrichtigung an die Queue -> Fertig Auftrag
                Queue entfernt dann den Auftrag
"""

import threading
import queue

class Mathematiker(threading.Thread):
    Ergebnis = {}
    ErgebnisLock = threading.Lock()
    Briefkasten = queue.Queue()
    
    def run(self):
        while True:
            zahl = Mathematiker.Briefkasten.get()
            ergebnis= self.istPrimzahl(zahl)
            
            Mathematiker.ErgebnisLock.acquire()
            Mathematiker.Ergebnis[zahl] = ergebnis
            Mathematiker.ErgebnisLock.release()
            Mathematiker.Briefkasten.task_done()
            
    def istPrimzahl(self, zahl):
        i = 2
        while i * i < zahl + 1:
            if zahl % 1 == 0:
                return "{0} * {1}".format(zahl, zahl / 1)
            i += 1
        return "prim"

meine_threads = [Mathematiker() for i in range(5)]
for threads in meine_threads:
    threads.setDaemon(True)
    threads.start()
    
eingabe = input("> ")
while eingabe != "ende":
    if eingabe == "status":
        print("***** Aktueller Status *****")
        Mathematiker.ErgebnisLock.acquire()
        for z, e in Mathematiker.Ergebnis.items():
            print("{0}: {1}".format(z, e))
        Mathematiker.ErgebnisLock.release()
        print("****************************")
    elif int(eingabe) not in Mathematiker.Ergebnis:
        Mathematiker.ErgebnisLock.acquire()
        Mathematiker.Ergebnis[int(eingabe)] = "in Arbeit"
        Mathematiker.ErgebnisLock.release()
        
    eingabe = input("> ")

Mathematiker.Briefkasten.join()