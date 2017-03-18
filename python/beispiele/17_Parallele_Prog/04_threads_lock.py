# -*- coding: utf-8 -*-

# LOESUNG -> LOCK-OBJEKT
# Critical Sections:
# Stellen, die nicht von mehreren Threads manipuliert werden duerfen

# Werden von der parameterlosen Funktion realisiert
# lock_Obj = _thread.allocate_lock() -> neues Lock-Objekt

# Wichtige Methoden:
    # acquire -> sperren
    # release -> entsperren

# So ist der Bereich save (synchronize)


import thread


anzahl_threads = 0
thread_gestartet = False

lock = thread.allocate_lock()

def naehere_pi_an(n):
    global anzahl_threads, thread_gestartet
    
    lock.acquire()
    anzahl_threads+= 1
    thread_gestartet = True
    lock.release()
    pi_halbe = 1
    zaehler, nenner = 2.0, 1.0
    for i in range(n):
        pi_halbe *= zaehler / nenner
        if i % 2:
            zaehler += 2
        else:
            nenner += 2
    print("Annaeherung mit {} Faktoren: {:.16f}".format(n, 2*pi_halbe))
    lock.acquire()
    anzahl_threads -= 1
    lock.release()
    
thread.start_new_thread(naehere_pi_an, (11111111,))
thread.start_new_thread(naehere_pi_an, (10000,))
thread.start_new_thread(naehere_pi_an, (100000,))
thread.start_new_thread(naehere_pi_an, (1234569,))
#thread.start_new_thread(naehere_pi_an, (), {"n" : 1337})

while not thread_gestartet:
    pass

while anzahl_threads > 0:
    pass

# Best Practise -> Alle relevanten Bereiche sichern durch lock
# Bei mehreren lock-Objekten kann es zum dead-Lock kommen
# durch Zugriff von 2 Threads auf dasselbe Objekt (Dauerwarten)