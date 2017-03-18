# -*- coding: utf-8 -*-

import _thread


# _threads bietet Funktion
# start_new_thread(function, args[,kwargs])
# Als Rückgabewert gibt _thread.start_new_thread eine Zahl zurück, die den
# erzeugten Thread eindeutig identifiziert.
# Nachdem function verlassen wurde, wird der Thread automatisch gelöscht.

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

_thread.start_new_thread(naehere_pi_an, (11111111,))
_thread.start_new_thread(naehere_pi_an, (10000,))
_thread.start_new_thread(naehere_pi_an, (100000,))
_thread.start_new_thread(naehere_pi_an, (1234569,))
_thread.start_new_thread(naehere_pi_an, (), {"n" : 1337})

while True:
    pass
# Die Endlosschleife am Ende des Programms ist notwendig, damit der Thread des
# Hauptprogramms auf die anderen Threads wartet und nicht sofort beendet wird.