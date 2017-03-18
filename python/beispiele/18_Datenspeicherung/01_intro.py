# -*- coding: utf-8 -*-

"""
Permanente Speicherung von Daten in verschiedensten Formaten
"""

# Das Modul gzip
# Daten packen und entpacken, die mit zlib-Bibliothek erstellt wurden

#gzip.open(filename[,mode[,compresslevel]])
# Gibt ein normal nutzbares Objekt zurueck
# compresslevel 0-9

import gzip
"""
# schreiben & packen
f = gzip.open("testdatei.gz", "wb")
f.write(b"Hallo Welt\r\n")
f.write(b"Zeile Zwei von Zwei")
f.close()
"""
# enpacken und lesen
g = gzip.open("testdatei.gz", "rb")
print(g.read().decode("utf-8"))

# Es gibt noch andere Module zur Verwaltung
# komprimierter Daten -> Nachlesen in Doku
# zlib
# gzip
# bz2
# zipfile
# tarfile

