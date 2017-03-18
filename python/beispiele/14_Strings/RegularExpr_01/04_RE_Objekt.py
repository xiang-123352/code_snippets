# -*- coding: utf-8 -*-


import re


# compile(pattern[, flags])
# kompiliert ein RegEx-Objekt
# lohnt sich bei mehreren Operationen mit demselben Pattern -> SpeedBoost
# Einflussnahme ueber Flags moeglich
# re.I -> IgnoreCase
# re.A -> ASCII - englisch
# re.L -> Locale (vom System)
# re.M -> Multiline
# re.S -> DOTALL -> . wird um \n erweitert
# re.U -> Unicode -> Standard seit Python3
# re.X -> Ignoiert alle Whitespace, die nicht maskiert wurden
#         Kann mit Kommentaren umgehen


c1 = re.compile(r"P[yY]thon")
# Bedeutet -> ein RE-Objekt c existiert, dem der RegEx r"P[Yy]th.n"
# zugrunde liegt
print(c1.match("Python"))
# -> <_sre.SRE_Match object; span=(0, 6), match='Python'>


# Flags
# Attribut flags ist eine ganze Zahl (alle gesetzten Flags)
# Alle zu setzenden Flags werden bei complie uebergeben
# Wenn kein flag uebergeben wird, dann ist der Wert standardmeassig 32
# das kommt durch standardgesetzte Flag re-UNICODE (Python 3.0)
print(c1.flags)
# Mit Flags
c2 = re.compile(r"P[y]thon", re.I)
print(c2.flags)
# Mit 2 Flags
c3 = re.compile(r"P[y]thon", re.I | re.S)
print(c3.flags)

# Verknuepfung mit UND -> Herausfinden, ob flag gesetzt wurde
# ja erg > 0
print(c2.flags & re.I) # Ja Bsp
print(c2.flags & re.M) # Nein Bsp


# groupindex
# Ist ein Dictionary, dass alle Gruppen enthaelt
# Namen, wenn vergeben, und der dazugehoerige Index
c4 = re.compile(r"(?P<gruppe1>P[Yy](?P<gruppe2>th.n))")
print(c4.groupindex)