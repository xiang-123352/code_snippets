# -*- coding: utf-8 -*-

"""
Erlaubt es XML-Dateien einzulesen und zu schreiben.
Gut lesbares Textformat.

Beispiel -> Inhalt eines Dictionarys dauerhaft speichern in XML

Die beiden im Modul xml enthaltenen Parser heißen dom und sax und
implementieren zwei unterschiedliche Herangehensweisen an das XML-Dokument.
Aus diesem Grund ist es sinnvoll, beide getrennt und ausführlich zu besprechen,
was in den nächsten beiden Abschnitten geschehen soll. Das Thema des dritten
Abschnitts ist eine weitere Python-spezifische Herangehensweise an XML-Daten
namens ElementTree.

"""

import xml.dom.minidom as dom
def knoten_auslesen(knoten):
    return eval("{}('{}')".format(knoten.getAttribute("typ"),
                knoten.firstChild.data.strip()))

def lade_dict(dateiname):
    d = {}
    with dom.parse(dateiname) as baum:
        if baum.firstChild.nodeName != "dictionary":
            return d
        
        for eintrag in baum.firstChild.childNodes:
            if eintrag.nodeName == "eintrag":
                schluessel = wert = None
                
                for knoten in eintrag.childNodes:
                    if knoten.nodeName == "schluessel":
                        schluessel = knoten_auslesen(knoten)
                    elif knoten.nodeName == "wert":
                        wert = knoten_auslesen(knoten)
                
                d[schluessel] = wert
    return d

lade_dict("ver1.xml")