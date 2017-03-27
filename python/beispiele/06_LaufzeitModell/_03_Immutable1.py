# -*- coding: utf-8 -*-

a = 1
b = 1
print(id(a))
print(id(b))
print(a is b)

# Ganzzahlen sind immutable
# Strings auch

var1 = "Wasser"
var1 += "flasche"
print(var1)

a = [1,2]
a += [3,4]
print(a)