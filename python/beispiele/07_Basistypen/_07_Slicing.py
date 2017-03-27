# -*- coding: utf-8 -*-

# SLICING (abschneiden)
# Mischen von pos. und neg.
string = "Ameisen"
# Buchstabe 2 - Ende
print(string[1:-1])

# Listen
L = ["Ich", "bin", "eine", "Liste", "von", "Strings"]
# Bei Listen ist -1 das vorletzte Feld
print(L[1:-1])

# Kurzschreibweise
s = "abcdefghijklmnopqrstuvwxyz"
# Ersten 5
print(s[:5])
# Alle ausser ersten 5
print(s[5:])

# KOPIEN ERZEUGEN
s1 = ["Doktorarbeit"]
# Keine Kopie
s2 = s1
print(s1 == s2)
print(s1 is s2)

# Wirkliche Kopie -> Identitaeten verschieden
s2 = s1[:]
print(s1 == s2)
print(s1 is s2)

# NUR BEI MUTABLE (IMMUTABLE IST ES EGAL, OB
# KOPIER ODER ORIGINAL (INHALT UNVERAENDERLICH)
s1 = "Kopiere mich"
s2 = s1[:]
print(s1 is s2)

# SONDERFALL SCHRITTWEITE
zahlen = "0123456789"
# von 1 bis 10(Ende) in 2er Schritten
print(zahlen[1:10:2])
# Kurzform
print(zahlen[1::2])

# Strings(Sequenz) umkehren
name = "ytnoM Python"
print(name[4::-1])
print(name[::-1])