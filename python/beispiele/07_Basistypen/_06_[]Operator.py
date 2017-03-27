# -*- coding: utf-8 -*-

# BEGINNT IMMER MIT 0

# Im String - > Wie in Java -> Index
alphabet = "abcdefghijklmnopqrstuvwxyz"
print(alphabet[9])

# In Liste - > Wie in Java -> Index
L = [1,2,3,4,5]
print(L[3])

# Umkehr -> Invertierung
# Letztes Feld wird mit -1 angesprochen
name = "Python"
print(name[-2])

# LISTE
L = [1, 2, 3, 4, 5, 6]
print(L[-1])

# Versucht man, mit einem Index auf ein nicht
# vorhandenes Element zuzugreifen, wird dies
# mit einem IndexError quittiert:
# IndexError: string index out of range
zukurz = "Ich bin zu kurz"
#print(zukurz[122])

# Es gehen auch Teilsequenzen
# INCL : EXCL
print(zukurz[4:7])

# Auch bei Listen
L = ["Ich", "bin", "eine", "Liste", "von", "Strings"]
print(L[1:4])