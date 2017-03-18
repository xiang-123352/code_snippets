# -*- coding: utf-8 -*-

"""
Bereitstellen von Programme / Modulen fuer andere Nutzer
Das Modul disutils

disutils automatisiert und standatisiert den Installationsprozess
Durch Erstellen von Distributionen

Es gibt zwei Typen
    - Quelldistribution (source distribution)
      - Archiv (enthaelt Quellcode des Moduls)
      - Installationsscript (setup.py)
      - herunterladen, entpacken, Script starten
      - Ist OS-unabhaengig, wenn so erstellt
      
    - Binaerdistribution (binary distribution)
      - ausfuehrbare Datei, die die Installation des Moduls automatisch
        durchfuehrt
      - Einfacher fuer Nutzer
      - Mehr AUfwand fuer Entwickler
      - Nicht mehr OS-unabheangig

Schritte zur Distribution
    - Schreiben des Moduls || Programms
    - Schreiben des Installationsscripts setup.py
    - Erstellen einer Quell- oder Binaerdistribution
"""

# Schreiben des Moduls
# Erinnerung an Unterschied Modul && Paket
# Modul -> einzelen Datei
# Paket -> Ordner mit mehreren Dateien (__init__.py)
