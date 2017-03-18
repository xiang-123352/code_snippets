# -*- coding: utf-8 -*-

# Instanziieren
string1 = b"Ich bin bytes!"
print(string1)
print(type(string1))

# byteArray
string2 = b"Hallo Welt"
string3 = bytearray(string2)
print(string3)

# leeres bytearray
print(bytearray(7))

# Mal ein Test
ziffern = "0123456789"
s = "3674784673546Versteckt zwischen Zahlen3425923935"
print(s.strip(ziffern))

#Format
zeit = "Es ist {0}:{1} Uhr".format(13, 37)
print(zeit)