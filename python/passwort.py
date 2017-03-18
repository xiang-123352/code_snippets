#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import hashlib

# Das Passwort lautet "Hallo Welt!"
pwhash = "578127b714de227824ab105689da0ed2"
m = hashlib.md5(raw_input("Ihr Passwort bitte: "))
if pwhash == m.hexdigest():
    print("Zugriff erlaubt")
else:
    print("Zugriff verweigert")
