# -*- coding: utf-8 -*-

"""
Reihenfolge von Buchstaben in Text vertauschen.
Ausser 1. und letzten.

@author:    Gyula Orosz
@func:      verwirble_Text()
@ver:       1.0.0
@date:      11.09.2016

@param:     text -> str || bytes-String
"""

import random

def verwirble_text(text):
    liste = []
    # Iteriert ueber die Liste
    for wort in text.split():
        # Jedes Wort zwischen dem 1. und letzten Buchstaben
        w = list(wort[1:-1])
        # Zufallsreihenfolge
        random.shuffle(w)
        # Wortliste zusammenfuegen
        liste.append(wort[0] + "".join(w) + wort[-1])
    # Wortliste zurueckgeben
    return " ".join(liste)