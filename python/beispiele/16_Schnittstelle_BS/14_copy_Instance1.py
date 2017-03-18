# -*- coding: utf-8 -*-

import copy as c

# Echte Kopie
#s = [1,2,3]
#t = c.copy(s)
#print(s is t)

# alles ok und wie erwartet
#liste = [1, [2, 3]]
#liste2 = c.copy(liste)
#liste2.append(4)
#print(liste)
#print(liste2)

# Manipulieren der inneren Liste -> nicht ok
#liste2[1].append(1337)
#print(liste)
#print(liste2)
#print(liste[1] is liste2[1])

# Loesung -> deepcopy
#liste = [1, [2, 3]]
#liste2 = c.deepcopy(liste)
#liste2.append(4)
#print(liste)
#print(liste2)
#print(liste[1] is liste2[1])

# Geaenderte MeineKlasse
class MeineKlasse:
    def __init__(self):
        self.Liste = [1,2,3]
        
    def getListe(self):
        return c.deepcopy(self.Liste)
        
    def zeigeListe(self):
        print(self.Liste)

# Original wird manipuliert
instanz = MeineKlasse()
liste = instanz.getListe()
liste.append(1337)
instanz.zeigeListe()