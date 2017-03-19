# -*- coding: utf-8 -*-

import urllib.parse

# Zerlegen einer URL
"""
url = "http://www.beispiel.de/pfad/zur/datei.py?prm=abc"
teile = urllib.parse.urlparse(url)
print(teile.scheme)
print(teile.netloc)
print(teile.path)
print(teile.params)
print(teile.query)
print(teile.fragment)
print(teile.hostname)
"""

#urllib.parse.parse_qs(qs[, keep_blank_values
#                     [, strict_parsing[, encoding[, errors]]]]),
# Aufbrechen der URL und Rueckgabe als Dictionary
#urllib.parse.parse_qsl(qs[, keep_blank_values
#                      [, strict_parsing[, encoding[, errors]]]])
# Aufbrechen der URL und Rueckgabe als Liste

# keep_blank -> Leere mit Aufnehmen?
# strict_parsing -> kleinere Fehler ignorieren?
# encoding und errors -> Umkodierung von Escape-Sequenzen steuern
"""
url = "http://www.test.de?hallo=welt&hallo=blubb&xyz=112"
teile = urllib.parse.urlparse(url)
print(urllib.parse.parse_qs(teile.query))
print(urllib.parse.parse_qsl(teile.query))
"""

# urllib.parse.urlunparse(parts) -> alles umgekehrt
#url = ("http", "www.test.de", "/pfad/datei.py", "", "", "")
#print(urllib.parse.urlunparse(url))

# urllib.parse.urlsplit(urlstring[, scheme[, allow_fragments]])
# identisch mit urlparse, ausser
# Attr params nicht in der Instanz vorhanden
# Parameter dem Pfad zugeordnet
# Sinnvoll bei neuer Syntax(Parameter an jedem Element des Pfades)

# urllib.parse.urljoin(base, url[, allow_fragments])
# Die Funktion urljoin kombiniert die Basis-URL base und die relative
# URL url zu einer absoluten Pfadangabe.

#base = "http://www.beispielGross.de"
#relativ = "pfad/zur/datei.py"
#print(urllib.parse.urljoin(base, relativ))
# Wird gnadenlos ueberschrieben, wenn base != base
#base = "http://www.test.de/hallo/welt.py"
#relativ = "du.py"
#print(urllib.parse.urljoin(base, relativ))


# urllib.parse.urldefrag(url)
# spaltet die Anker ab, wenn vorhanden
# Rueckgabe -> Tuple
#print(urllib.parse.urldefrag("http://www.test.de#frag"))
#DefragResult(url='http://www.test.de', fragment='frag')

# urllib.parse.quote(string[, safe[, encoding[, errors]]])
# ersetzt unerlaubte Sonderzeichen durch konforme(%20...)
# safe -> String -> nicht umzuwandelnde Zeichen
# encode und errors -> Wie wird mit string umgegangen?
# Standard utf-8 und strict
#print(urllib.parse.quote("www.test.de/hallo welt.html"))

# urllib.parse.unquote(string[, encoding[, errors]])
# Umkehrfunktion zu quote
#print(urllib.parse.unquote("www.test.de/hallo%20welt.html"))

# urllib.parse.urlencode(query[, doseq[, safe[, encoding[, errors]]]])
# erzeugt aus den KV des query einen String mit dem Format
# RV kann als data der Funktion urlopen oder urlretrieve uebergeben werden
#print(urllib.parse.urlencode({"abc" : 1, "def" : "ghi"}))

# Wenn das Dict eine Sequenz enthaelt und doseq==True
#print("True: " + urllib.parse.urlencode({"abc" : [1,2,3],
#                                         "def" : "ghi"},
#                                         True))
#print("False: " + urllib.parse.urlencode({"abc" : [1,2,3],
#                                          "def" : "ghi"},
#                                          False))