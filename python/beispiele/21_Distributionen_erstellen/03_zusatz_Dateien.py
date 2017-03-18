# -*- coding: utf-8 -*-

"""
Falls neben Modulen und Paketen noch Dateien zum Projekt
gehoeren, muessen diese auch in die Distribution geschrieben werden

In erster Linie Scriptdateien
(Implementation von Tools, die was mit dm Paket zu tun haben)

Modul  -> stellt mir Funktionen oder Klassen zur Verfuegung
          fuehrt keinen Python-Code aus

Script -> enthaelt ein lauffaehiges Programm

distutils-Paket installiert Scripte in ein Verzeichnis,
indem sie systemweit ausfuehrbar sind

Werden in der setup.py mit kw-param scripts uebergeben
(Liste von Strings)

Bonus: distutils passt automatisch die Shebang-Zeile an das BS an

Ressourcen: Sind Dateien, die von bestimmten Paketen benoetigt werden...
            z.B. hallo.txt, test.txt in paket1
            package_data = {"paket1" : ["hallo.txt", "welt.txt"]}
            Wildcards funktionieren auch *.txt

sonstige Daten: Alle Daten, die in keine vorherige Kategorie passen...
                z.B. Konfigurationsdateien, Hilfeseiten o.a.
                Schluesselwort data_files
                setup(
                     [...]
                     data_files = [("grafiken", ["test1.bmp", "test2.bmp"]),
                                   ("config", ["programm.cfg"])]
                     )
                test1.bmp und test2.bmp aus grafiken wird in Distri uebernommen
                programm.cfg aus config wird in Distri uebernommen
                Alles relativ zum Pfad des Install-Scripts
                Absolute gehen auch -> z.B. systemweite Config-Datei
                
                Wenn kein absoluter Pfad angegeben wurde,
                landen alle in data_files angegebenen Dateien...
                in Windows -> Pythonverzeichnis
                in Linux -> /usr

Ordner innerhalb von Pfaden immer mit / trennen
distutils kuemmert sich um die korrekte Umsetzung
"""