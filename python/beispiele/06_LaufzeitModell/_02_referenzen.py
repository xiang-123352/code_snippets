# -*- coding: utf-8 -*-

# ID (Eindeutige Zuweisung)
a = 1
b = 1
print(id(a))
print(id(b))
print(a is b)

#Referenzen freigeben
print(a)
del a
# a is not defined
#print(a)

# auch kommasepariert moeglich
v1 = 123
v2 = 456
v3 = 789
del v1, v2, v3
