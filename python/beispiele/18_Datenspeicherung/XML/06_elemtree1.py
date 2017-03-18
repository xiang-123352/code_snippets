# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ElementTree

def lese_text(element):
    typ = element.get("typ", "str")
    return eval("{}('{}')".format(typ, element.text))

def lade_dict(dateiname):
    d = {}
    baum = ElementTree.parse(dateiname)
    tag_dict = baum.getroot()
    for eintrag in tag_dict:
        tag_schluessel = eintrag.find("schluessel")
        tag_wert = eintrag.find("wert")
        d[lese_text(tag_schluessel)] = lese_text(tag_wert)
    return d

lade_dict("ver2.xml")
print(lese_text("schluessel"))