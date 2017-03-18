# -*- coding: utf-8 -*-

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

# Dieser Ausdruck ermittelt den Namen des Datentyps der von schluessel
# referenzierten Instanz. Das wäre beispielsweise "int" für ganze Zahlen oder
# "str" für Strings. Jetzt folgt die Hauptfunktion des Beispielprogramms:
def erstelle_eintrag(schluessel, wert):
    tag_eintrag = dom.Element("eintrag")
    tag_schluessel = dom.Element("schluessel")
    tag_wert = dom.Element("wert")
    
    tag_schluessel.setAttribute("typ", type(schluessel).__name__)
    tag_wert.setAttribute("typ", type(wert).__name__)
    
    text = dom.Text()
    text.data = str(schluessel)
    tag_schluessel.appendChild(text)
    
    text = dom.Text()
    text.data = str(wert)
    tag_wert.appendChild(text)
    
    tag_eintrag.appendChild(tag_schluessel)
    tag_eintrag.appendChild(tag_wert)
    return tag_eintrag
    
def schreibe_dict(d, dateiname):
    baum = dom.Document()
    tag_dict = dom.Element("dictionary")
    
    for schluessel, wert in d.items():
        tag_eintrag = erstelle_eintrag(schluessel, wert)
        tag_dict.appendChild(tag_eintrag)
        
    baum.appendChild(tag_dict)
    
    with open("ver3.xml", "w") as f:
        baum.writexml(f, "", "\t", "\n")

dict1 = {}
dict1 = erstelle_eintrag("Artist", "Bon Jovi")
dict1 = erstelle_eintrag("Artist", "Metallica")
dict1 = erstelle_eintrag("Artist", "Manowar")
schreibe_dict(dict1, lade_dict("ver3.xml"))