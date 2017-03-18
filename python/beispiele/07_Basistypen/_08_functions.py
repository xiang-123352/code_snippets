# -*- coding: utf-8 -*-

# Funtionen von Sequenzen
string = "Wie lang bin ich wohl?"
print(len(string))

# Anzahl der Elemente
zahl = len(["Hallo", 5, 2, 3, "Welt"])
print(zahl)

# min und max
L = [5,1,10,-9.5,12,-5]
print(max(L))

print(min(L))

# Fehler
#l = [1,2, "welt"]
#print( min(l) )

# Geht auch bei Strings
print( max("Wer gewinnt wohl"))
print( min("Zeichenkett"))

# Position (index)
ziffern = [1, 2, 3, 4, 5, 6, 7, 8, 9]
zahl = ziffern.index(3)
print(zahl)

# Geht auch bei String
s = "Hallo Welt"
foundAt = s.index("l")
print(foundAt)

# Mit Parameter Start-Ende
ziffer = [1, 22, 333, 4444, 333, 22, 1].index(1, 3, 7)
# Suche 1 zwischen block 3 und 7
# ab 333 ( index4 )
print(ziffer)
zahl = "Hallo Welt".index("l", 5, 100)
# hinter Hallo
print(zahl)

# Anzahl mit count
s = [1, 2, 2, 3, 2]
print(s.count(2))
print("Hallo Welt".count("l"))
