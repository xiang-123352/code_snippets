# -*- coding: utf-8 -*-


# Schwachstellen ausmerzen


import threading

class PrimzahlThread(threading.Thread):
    Ergebnis = {}
    ErgebnisLock = threading.Lock()
    
    def __init__(self, zahl):
        threading.Thread.__init__(self)
        self.Zahl = zahl
        
        PrimzahlThread.ErgebnisLock.acquire()
        PrimzahlThread.Ergebnis[zahl] = "in Arbeit"
        PrimzahlThread.ErgebnisLock.release()
        
    def run(self):
        i = 2
        while i*i <= self.Zahl:
            if self.Zahl % i == 0:
                ergebnis = "{0} * {1}".format(i, self.Zahl / i)                
                PrimzahlThread.ErgebnisLock.acquire()
                PrimzahlThread.Ergebnis[self.Zahl] = ergebnis
                PrimzahlThread.ErgebnisLock.release()               
                
                return
            i += 1
        
        PrimzahlThread.ErgebnisLock.acquire()
        PrimzahlThread.Ergebnis[self.Zahl] = "prim"
        PrimzahlThread.ErgebnisLock.release() 


meine_threads = []
eingabe = input("> ")

# Benutzereingabe -> Pruefen auf Eingabe ende
# Neuer Thread wird mit eingabe als Parameter erzeugt
# und mit start() gestartet
while eingabe != "ende":
    if eingabe == "status":
        print("===== Aktueller Status =====")
        PrimzahlThread.ErgebnisLock.acquire()
        for z, e in PrimzahlThread.Ergebnis.items():
            print("{0} = {1}".format(z, e))
        PrimzahlThread.ErgebnisLock.release()
        print("============================")
        
    elif int(eingabe) not in PrimzahlThread.Ergebnis:
        thread = PrimzahlThread(int(eingabe))
        #Liste aller Threads
        meine_threads.append(thread)
        thread.start()
        
    eingabe = input("> ")

for t in meine_threads:
    # Warten bis alle fertig sind (der aufrufende wurde terminiert)
    t.join()