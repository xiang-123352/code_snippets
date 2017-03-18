# -*- coding: utf-8 -*-

# mutabler Datentyp

# Ueberschreiben
s = [1, 2, 3, 4, 5, 6, 7]
s[3] = 1234
print(s)

# Ersetzen Adden
einkaufen = ["Brot", "Eier", "Milch", "Fisch", "Mehl"]
# statt Eier und Milch
# Wasser und Wurst
einkaufen[1:3] = ["Wasser", "Wurst"]
print(einkaufen)

# Slicing
s = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# 2 bis 9 schrittweite 3
s[2:9:3] = ["A", "B", "C"]
print(s)

# loeschen
del s[0:5]
print(s)

# loeschen gerader Index
s = ["a","b","c","d","e","f","g","h","i","j"]
del s[::2]
print(s)

# SideEffects bei Listen
a = [[]]
a = 4 * a
print(a)
# Durch das Duplizieren der einen
# Verhalten sich alle 4 wie eine einzige
a[0].append(10)
print(a)