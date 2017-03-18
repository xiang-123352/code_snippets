# -*- coding: utf-8 -*-

"""
Eine URL (für Uniform Resource Locator) spezifiziert eine Ressource,
beispielsweise im Internet, über ihren Ort und das zum Zugriff zu verwendende
Protokoll. Das Paket urllib bietet eine komfortable Schnittstelle zum Umgang
mit Ressourcen im Internet. Dazu enthält urllib die folgenden Module:
"""
# urllib.request
# urllib.response
# urllib.parse
# urllib.error
# urllib.robotparser

import urllib.request
# urllib.request.urlopen(url[, data][, timeout], *, [cafile][capath])
# Dateiobjekt, auf dem keine Schreibrechte existieren
# Moeglichkeit Quelltext einer Webseite herunterzuladen
# Automatisch file:// wenn keine Angabe von http:// oder ftp://
# Wenn Ress nicht exists -> IOError
# dateiaehnliches Objekt (file-like-object)
# Nicht alle Methoden eines richtigen Objektes verfuegbar (Untermenge)
    # read([size])
    # readline([size])
    # readlines([sizehint])
    # fileno()
    # close()
    # info()
    # geturl()
#f = urllib.request.urlopen("http://www.galileo-press.de")
# info() = dictionary-aehnliche Objekt
#d = f.info()
#print(d)
#print(d.keys())
#print(d["Content-Length"])
#print(d["Server"])

# falls http -> optionale Parameter data
# POST-Parameter
# urlencode() zum Aufbereiten aus urllib.parse
#prm = urllib.parse.urlencode({"prm1":"wert1", "prm2":"wert2"})
#f = urllib.request.urlopen("http://beispiel.de", prm)

# Geht auch mit GET
#f = urllib.request.urlopen("http://Beispiel.de?prm=wert")

# Timeout ist auch ein optionaler Param
# Besagt, wie lange urlopen auf die Antwort des Servers wartet
# ohne -> Standardwert des BS

# cafile und capath sind reine Schluesselwortparameter
# erlaube es, Zertifikate bereitzustellen, ueber die sich
# urlopen bei der Gegenstelle authentifizieren kann
# cafile -> Pfad zur Datei
# capath -> Pfad zum Ordner

# urllib.request.urlretrieve(url[, filename[, reporthook[, data]]])
# Inhalt der Ress wird lokal verfuegbar gemacht unter filename
# dazu wird Ress runtergeladen, falss nicht schon vorhanden
# Rueckgabe = Tuple (DateiName_lokaleDatei, RV_info())

#print(urllib.request.urlretrieve("http://www.galileo-press.de"))

#('C:\\Users\\gyula\\AppData\\Local\\Temp\\tmpg7h19r_2',
# <http.client.HTTPMessage object at 0x00D7B2B0>)

# Bei Eingabe eines Namen, kann man entscheiden, wohin die geladene
# Ressource kopiert werden soll, sonst tmp-Verzeichnis des BS

# dritter Param kann ein Funktionsobjekt sein. -> wird 1x aufgerufen,
# wenn die Verbindung zur NW-Ress hergestellt wurde.
# und dann so oft wie benötigt
# 3 Parameter bei Callback-Funktion -> 
# Anzahl Blocks(fertig), Groesse Block, Gesamtanzahl Blocks (Statusanzeige)

"""
def f(blocks, blocksize, size):
    print("Status: {}%".format(int(blocksize*blocks*100/size)))
    
url = "http://www.galileo-press.de"
res = urllib.request.urlretrieve(url, "datei.html", f)
print(res)
# Das letzte Paket hat nicht die volle Groesse, wird aber so berechnet
"""

# urllib.request.FancyURLopener([proxies][, **args])
# Falls Authentifizierung am Server benoetigt wird
# oder falls ueber einen Proxy gegangen werden muss
# Attr proxies -> Dictionary mit KV ->
# {"http": "http://proxy.beispiel.de:8080/"}
# key_file(Schluessel) und cert_file(Zertifikat) Parameter bei SSL Verbindung
"""
class MyURLopener(urllib.request.FancyURLopener):
    def __init__(self, proxies=None, **args):
        urllib.request.FancyURLopener.__init__(self, proxies, **args)
    
    def prompt_user_passwd(self, host, realm):
        return ("username", "password")

opener = MyURLopener()
f = opener.open("http://www.beispiel.de")
print(f.read())
"""