#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib

# Das Passwort lautet "Hallo Welt!"
pwhash="578127b714de227824ab105689da0ed2"

#m = hashlib.md5((input("Ihr Passwort bitte: ")).encode())
m = hashlib.md5(bytes(input("Ihr Passwort bitte: "), "utf-8"))
print(m.hexdigest())
if pwhash == m.hexdigest():
    print("Zugriff erlaubt")
else:
    print("Zugriff verweigert")
