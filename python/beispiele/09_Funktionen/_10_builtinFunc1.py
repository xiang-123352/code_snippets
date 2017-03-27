# -*- coding: utf-8 -*-

# Betrag bilden (absolut Wert)
print(abs(-100))

# Pruefen, ob ALLE wahr bei Iterable
print(all([True, True, False]))

# Pruefen, ob mind. 1 wahr beio Iterable
print(any([True, False, False]))

#ascii
print(ascii(range(0, 10)))
print(ascii("Püthon"))
print(repr("Püthon"))

#bin
print(bin(123))
print(bin(-12))
print(bin(0))

#bytearray
print(bytearray("äöü", "utf-8"))
print(bytearray([1,2,3,4]))
print(bytearray(10))

#bytes
print(bytes("äöü", "utf-8"))
print(bytes([1,2,3,4]))
print(bytes(10))

#character
print(chr(65))
print(chr(33))
print(chr(8364))

#complex
print(complex(1,3))
print(complex(1.2,3.5))
print(complex("3+4j"))	#ohne Leerzeichen
print(complex(3))