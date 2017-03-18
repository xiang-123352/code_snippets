# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 10:06:54 2016

@author: gyula
"""

# RegEx ist in Python ein String, der die Regel enthaelt
# Immer Python Raw-Strings nehmen
# r".ython"

s = r"*Py\.\.\.on"
# passt nur auf "Py...on"

s = "xaababcbcd"
sub = "abc"
# pruefen ob s[0] == sub[0]
# erstes Feld des Pattern zählt -> nur 1x anfassen
# immer weiterschieben

# Escape Sequenzen -> AUFPASSEN !!!!
# Oder Auswertung untersagen fuer das Zeichen