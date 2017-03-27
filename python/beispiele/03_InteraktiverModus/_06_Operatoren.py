# -*- coding: utf-8 -*-
# arithmetisch
a = 7
b = 4
c = a + b
d = a - b
e = a * b
f = a / b
g = a // b
h = a % b

# Logische (Auswertung immer boolean)
if(a > b):
	print("a > b")
if(a >= b):
	print("a >= b")
if(a < b):
	print("a < b")
if(a <= b):
	print("a <= b")
if(a != b):
	print("a != b")
if(a == b):
	print("a == b")

#not
print(not(3 < 4))

# and ( beide Seiten müssen True ergeben fuer True)
print( (3 < 4) and (5 < 6))

# or (mind. 1 Seite muss True ergeben fuer True)
print( (3 > 4) or (5 > 6))