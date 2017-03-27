# -*- coding: utf-8 -*-

# Dictionary
print(dict({"a" : 1, "b" : 2}))

# auch aus Tuple
print(dict([("a",1),("b",2)]))

# als kwargs
print(dict(a=1, b=2))

# divmod(a,b)
# ist Tuple(a//b, a%b)
print(divmod(2.5,1.3))
print(divmod(11,4))

# enumerate(iterable)
# durch Nummerierung von Null beginnend
print(list(enumerate(["a", "b", "c", "d"])))

# gut geeignet fuer for-Schleifen
iterable = [1,2,3,4,5]
for i, wert in enumerate(iterable):
	print("Der Wert von iterable an", i, ". Stelle ist: ", wert)

# filter(function, iterable)
# alle geraden Zahlen bis 21
filterobj = filter(lambda x : x % 2 == 0, range(21))
print(list(filterobj))

# floats
print(float())
print(float("0.5"))

# format(value[,format_spec])
print(format(1.23456, ".2f") + "€")

# Frozenset (immutable Set)
print(frozenset())
print(frozenset({1,2,3,4,5}))
print(frozenset("Pyyyyyyyyython"))

# globals
a = 1
b = {}
c = [1,2,3]
print(globals())