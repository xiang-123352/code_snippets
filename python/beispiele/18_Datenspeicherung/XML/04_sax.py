# -*- coding: utf-8 -*-

import xml.sax as sax

"""
- self.ergebnis     für das resultierende Dictionary
- self.schluesse    für den Inhalt des aktuell bearbeiteten Schlüssels
- self.wert         für den Inhalt des aktuell bearbeiteten Wertes
- self.aktiv        für den Tag-Namen des Tags, das zuletzt eingelesen wurde
- self.typ          für den Datentyp, der im Attribut typ eines schluessel-
                    oder wert-Tags steht
"""

class DictHandler(sax.handler.ContentHandler):
    
    def __init__(self):
        self.ergebnis = {}
        self.schluessel = ""
        self.wert = ""
        self.aktiv = None
        self.typ = None

    def startElement(self, name, attrs):
        if name == "eintrag":
            self.schluessel = ""
            self.wert = ""
        elif name == "schluessel" or name == "wert":
            self.aktiv = name
            self.typ = eval(attrs["typ"])

    def endElement(self, name):
        if name == "eintrag":
            self.ergebnis[self.schluessel] = self.typ(self.wert)
        elif name == "schluessel" or name == "wert":
            self.aktiv = None

    def characters(self, content):
        if self.aktiv == "schluessel":
            self.schluessel += content
        elif self.aktiv == "wert":
            self.wert += content

    def lade_dict(dateiname):
        handler = DictHandler()
        parser = sax.make_parser()
        parser.setContentHandler(handler)
        parser.parse(dateiname)
        return handler.ergebnis

