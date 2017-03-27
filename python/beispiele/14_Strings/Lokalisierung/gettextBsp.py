# -*- coding: utf-8 -*-

"""
Created on Fri Jul 29 11:42:17 2016

@author: gyula

Das Modul gettext nuetzt bei Internationalisierung und Lokalisierung.
Kann somit leicht an sprachliche und kulturelle Gegebenheiten angepasst werden.
Beschraenkt sich auf die Uebersetzung von Strings.
Datum- und Waehrungsformate nicht beruecksichtigt.

- Programmer schreibt seine Applikation
- String werden durch Wrapper-Funktion geschickt
- function({englishWord}: str) -> deutschesWort:str
"""


# Beispiel:
# Lies solange User-Eingaben bis Enter ohne Worteingabe vorher.
import gettext
import random


# Hier wird eine Translation-Objekt mit <gettext.transloation> erstellt
# Der Name wird auch Domain genannt ist der erste Parameter
# 2.Parameter ist das Unterverzeichnis, indem sich die Uebersetzungen befinden
# 3.Parameter ist eine Liste von Sprachen
# Das Translation-Objekt uebersetzt nun in die 1.Sprache, fuer
# die ein Sprachkompilat gefunden werden kann
trans = gettext.translation("meinprogramm", "locale", ["de"])

# Durch install wird lokale Funktion _ geladen, mit der dann die
# String uebersetzt werden
trans.install()

# Hinweis
# Bei der print-Ausgabe am Ende des Beispielprogramms wird die Funktion _ für
# einen mit einem Platzhalter behafteten String aufgerufen, bevor dieser
# Platzhalter durch dynamischen Inhalt ersetzt wird. Das ist wichtig, da sonst
# keine Übersetzung erfolgen kann.

# Erstellen eines Sprachkompilats
# Liste aller zu uebersetzender Strings erstellen
# händisch eklig -> Programm pyggettext.py
# Erstellt *.po (lesbare *.mo)

# Leere *.po erstellen
# Danach
# python msgfmt {name.po}
# es wird eine name.mo an derselben Stelle erstellt

t = gettext.translation('meinprogramm', 'locale', ["de"])
_ = t.gettext
#print(_('Please enter a value: '))

werte = []
while True:
    w = input(_("Please enter a value: "))
    if not w:
        break
    werte.append(w)
print(_("The random choice is {0}").format(random.choice(werte)))