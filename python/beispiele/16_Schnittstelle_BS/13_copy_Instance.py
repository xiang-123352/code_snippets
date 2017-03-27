# -*- coding: utf-8 -*-

"""
Normalerweise wird nicht kopiert, sondern nur eine neue
Referenz zugewiesen. Das ist nicht immer so gewollt.
"""

# s und t referenzieren dieselbe Liste (Sideeffects)
#s = [1,2,3]
#t = s
#print(t is s)

class MeineKlasse:
    def __init__(self):
        self.Liste = [1,2,3]
        
    def getListe(self):
        return self.Liste
        
    def zeigeListe(self):
        print(self.Liste)

# Original wird manipuliert
instanz = MeineKlasse()
liste = instanz.getListe()
liste.append(1337)
instanz.zeigeListe()