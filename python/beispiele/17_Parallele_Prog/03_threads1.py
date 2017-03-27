# -*- coding: utf-8 -*-

import thread


# threads bietet Funktion
# start_newthread(function, args[,kwargs])
# Als Rückgabewert gibt thread.start_newthread eine Zahl zurück, die den
# erzeugten Thread eindeutig identifiziert.
# Nachdem function verlassen wurde, wird der Thread automatisch gelöscht.

anzahlthreads = 0

def naehere_pi_an(n):
    global anzahlthreads
    anzahlthreads += 1
    pi_halbe = 1
    zaehler, nenner = 2.0, 1.0
    for i in range(n):
        pi_halbe *= zaehler / nenner
        if i % 2:
            zaehler += 2
        else:
            nenner += 2
    print("Annaeherung mit {} Faktoren: {:.16f}".format(n, 2*pi_halbe))
    anzahlthreads -= 1

thread.start_new_thread(naehere_pi_an, (11111111,))
thread.start_new_thread(naehere_pi_an, (10000,))
thread.start_new_thread(naehere_pi_an, (100000,))
thread.start_new_thread(naehere_pi_an, (1234569,))
#thread.start_new_thread(naehere_pi_an, (), {"n" : 1337})



while anzahlthreads > 0:
    pass

# Es ist nicht sauber.Beide Zeilen, wo die globale Variable anzahlthreads
# geaendert wird, sind unsicher.
# Wert lesen -> neue Instanz(+1|-1)-> Referenz neu verknuepfen
# keine atomare Abarbeitung (ungenau -> Ueberschneidungen)