# -*- coding: utf-8 -*-

vorname = "Heinz"
nachname = "Kugel"
name = vorname + " " + nachname
print(name)

s = "Musik"
s += "stück"
print(s)

# IMMUTABLE str
s = "Musik"
t = "stück"
temp = s
s += t
# Instanz s
print(s)
# Instanz t
print(t)
# Instanz temp
print(temp)

# MUTABLE list
s = [1,2]
t = [3,4]
temp = s
s += t
# Instanz s
print(s)
# Instanz t
print(t)
# Instanz temp ( s und temp verweisen auf dieselbe Instanz)
print(temp)