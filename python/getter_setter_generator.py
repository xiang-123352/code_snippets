#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys

def generate_getter(attr):
    attr = attr.lower()
    
    print("def _get_" + attr + "(self):")
    print("    return self." + attr.capitalize())
    print("")

def generate_setter(attr):
    attr = attr.lower()
    
    print("def _set_" + attr + "(self, " + attr + "):")
    print("    self." + attr.capitalize() + " = " + attr + " ")
    print("")

def generate_property(attr):
    attr = attr.lower()
    
    print(attr + " = property(_get_" + attr + ", _set_" + attr + ")")
    print("")

def generate_get_set_property(liste):
    for attr in liste:
        generate_getter(attr)
        generate_setter(attr)
        generate_property(attr)

sys.stdout = open("output.py", "wt")

film = ['Title', 'Erscheinungsjahr', 'Dauer', 'Bewertung', 'FSK', 'Beschreibung', 'Kurzbeschreibung', 'Genre', 'Personen', 'Produktionsland', 'Sprachen']
personen = ['Nachname', 'Vorname', 'Herkunft', 'Regisseur']
produktionsland = ['Land']
sprachen = ['Sprache', 'Untertitel']

generate_get_set_property(sprachen)

f.close()
