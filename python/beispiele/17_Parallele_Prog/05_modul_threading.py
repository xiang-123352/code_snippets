# -*- coding: utf-8 -*-

# Jeder Thread ist eine Instanz einer Klasse, die von
# threading.Thread erbt
# Die Klasse selbst ist Teil eines globalen Namensraumes.
# Die statischen Member eignen sich gut zum Austausch zwischen
# den Threads -> Sichern durch locks

# Die Klasse threading.Thread hat eine Methode start()
# startet den Thread
# run() -> Was wird gemacht

import threading

class PrimzahlThread(threading.Thread):
    def __init__(self, zahl):
        threading.Thread.__init__(self)
        self.Zahl = zahl
        
    def run(self):
        i = 2
        while i*i <= self.Zahl:
            if self.Zahl % i == 0:
                print("{0} ist nicht prim, da{1} = {2} * "
                      "{3}".format(self.Zahl, self.Zahl, i, self.Zahl // i))
                return
            i += 1
        print("{0} ist prim".format(self.Zahl))


meine_threads = []
eingabe = input("> ")

# Benutzereingabe -> Pruefen auf Eingabe ende
# Neuer Thread wird mit eingabe als Parameter erzeugt
# und mit start() gestartet
while eingabe != 0:
    thread = PrimzahlThread(int(eingabe))
    #Liste aller Threads
    meine_threads.append(thread)
    thread.start()
    eingabe = input("> ")

for t in meine_threads:
    # Warten bis alle fertig sind (der aufrufende wurde terminiert)
    t.join()

print(meine_threads)