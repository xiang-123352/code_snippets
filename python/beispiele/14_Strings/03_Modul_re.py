# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 13:36:54 2016

@author: gyula
"""

# Verwendung
# Einbinden 
import re
# Funktion escape
satz = re.escape("Geht das wirklich?")
print(satz)


# Funktion findall
# Wort wird gefunden und ausgegeben jedesmal. Bei Gruppen nur die Treffer der
# Gruppe (Tuple)
satz1 = re.findall(r"P[Yy]thon", "Python oder PYthon und Python")
print(satz1)
# mit Gruppe
satz2 = re.findall(r"P([Yy])thon", "Python oder PYthon und Python")
print(satz2)
# mit 2 Gruppen
satz3 = re.findall(r"P([Yy])th(.)n", "Python oder PYthon und Python")
print(satz3)


# Funktion match
# Wenn Uebereinstimmung gefunden wird,
# wird ein Match-Objekt erzeugt, sonst None
print(re.match(r"P[Yy]thon", "PYYthon"))
print(re.match(r"P[Yy]thon", "PYthon"))


# Funktion search
# Durchsucht einen String nach einem Teilstring
# Rueckgabe ist auch ein Match-Objekt bei erstem Fund/Treffer, sonst None
print(re.search(r"P[Yy]thon", "Nimm doch Python"))


# Funktion split -> split
# split(pattern, string, maxsplit=0, flags=0)
# Ausgabe Trennzeichen bei Gruppierung, sonst nicht
print(re.split(r"\s", "Python Python Python"))
# Gruppen splitten
print(re.split(r"(,)\s", "Python, Python, Python"))


# sub(pattern, repl, string, count=0, flags=0)
print(re.sub(r"[Jj]a[Vv]a","Python", "Java oder java und jaVa"))
# Was , Wodurch und Worin
# Man kann auch fuer repl eine Funktion uebergeben
def f(m):
    return "x" * len(m.group(0))
# Wenn in irgendeinem Wort "sex" vorkommt,
# wird das ganze Wort mit x ueberschrieben
a = re.sub(r"\b(\w*?sex\w*?)\b", f , 
            "Wirtschaftsexperten auf Arktisexpedition")
print(a)
# \g<name> oder \g<index> koenner auch genutzt werden
print(re.sub(r"([Jj]ava)","Python statt \g<1>", "Nimm doch Java"))
# Bei welchem Teil, Wird welcher einegfuegt und in welchem String


# subn(pattern, repl, string[, count])
# Gibt immer ein Tupel zurueck und die Anzahl der Ersetzungen
print(re.subn(r"([Jj]ava)","Python statt \g<1>", "Nimm doch Java"))