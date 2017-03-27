# -*- coding: utf-8 -*-

"""
Hash-Funktionen - hashlib

Sind komplexe Algorithmen, die aus Strings Hashwerte berechnen.
Sind Sicherheitsmechinismen, um z.B. PWs in Datenbanken nicht
in Klartext lesen zu koennen.

Eine Hashfunktion wird mit einem Parameter aufgerufen und errechnet
fuer diesen String(Parameter) den Hashwert.

- Ist eine Einweg-Kodierung 
    - Man kann nicht aus dem Hash-Wert auf die OriginalInformationen schliessen
- Es treten prinzipiell Kollosionen auf (2 gleiche HashWerte)
    - Dies sollte erschwert werden
        - z.B. durch Salts (RandomZahl am Passwort vor HashWert-Generierung)
- Hash-Funktionen sollten willkuerlich sein
    - Kein erkennbares Muster -> keine Rueckschluesse
- Schnell berechenbar -> Schnell vergleichbar
"""

# Die Verwendung der Klassen ist identisch
# Hier Beispiel fuer md5

import hashlib

# Beim Instanziieren wird eine bytes-Instanz uebergeben
# Seit Python 3.0 geht das mit reinen Strings nicht mehr
md5 = hashlib.md5(b"Hallo Welt")

# Ausgabe als Bytefolge (auch nicht druckbare Zeichen)
print(md5.digest())
# b'\\7*2\xc9\xaet\x8aL\x04\x0e\xba\xdcQ\xa8)'

# Ausgabe als String mit hexdigest (nur druckbare Zeichen)
print(md5.hexdigest())
# 5c372a32c9ae748a4c040ebadc51a829

print(__doc__)