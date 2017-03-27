# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 13:06:54 2016

@author: gyula
"""

# Extensions
# Gruppierungs Syntax mit ? -> (?...)
# Normalerweise so nicht bekannt
# Nutzen von Flags
# Flag ->   i       -> case insensitive
#           :       -> Gruppen ohne Overhead (Keine Ueberlagerung)
#           P<name> -> Namen vergeben und darueber zugreifen
#                      Aufruf r"(?P=<name>))
#           #       -> Kommentare
#                      r"Py(?#lalala)thon"
#           =       -> Passt nur, wenn Nachfolger auch passt
#                      r"\w+(?= Meier)"
#           !       -> Negation
#           <=      -> Pruefung mit Vorgaenger
#           <!      -> Ungleich Vorgaenger

#   Spezial Fall -> Ternär
#   (?(id/name)yes-pattern[|no-pattern])
#   r"(?P<klammer>\()?Python(?(klammer)\))
#   Suchen nach Python in Klammern