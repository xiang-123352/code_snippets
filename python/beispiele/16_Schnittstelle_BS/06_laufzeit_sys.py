# -*- coding: utf-8 -*-

"""
- Stellt Variablen und Funktionen, die sich auf den Python-Interpreter
  beziehen oder eng mit ihm zusammenhaengen
- Abfragen Versionsnummer Interpreter und BS

 - Enthaelt eine Reihe von Konstanten
"""

import sys

# argv -> Enthaelt Kommandozeilen Parameter, mit denen das
# Python Programm gestartet wurde
#   argv[0] = name des Programms
#   programm.py -bla 0 -blubb abc
#   ['programm.py', '-bla', '0', '-blubb', 'abc']
# Fuer die Verwaltung nutzt man argparse()

# byteorder -> spezifieziert die Byte-Order
#   big     -> Big-Endian-System (Speicherung signifikanteste Byte)
#   little  -> Little-Endian-System (Speicherung des am wenigsten
#              signifikanteste Byte)

# executable -> Pfad zur ausfuehrbaren Datei des Python-Interpreters
print(sys.executable)

# hexversion -> Versionsnummer des P-Interpreters als Hex
# Version 3.4.4 -> zum Ueberpruefen der Kompatibilitaet
print(hex(sys.hexversion))

# path .> Liste enthaelt Pfadangaben, die beim Einbinden des Moduls
# der Reihe nach vom Interpreter durchsucht werden
print(sys.path)

# platform -> Kennung BS
print(sys.platform)

# stdin, stdout, stderr
# Sind Datei-Objekte des Interpreters
#   stdin  -> Standard input
#   stdout -> Standard Output
#   stderr -> Standard Error
# Durch Ueberschreiben -> Umleiten moeglich
# stdin muss ein vollwertiges Objekt sein
# stdout und stderr reicht Instanzen, die eine Methode write
# implementiert
# Urspruengliche Stream gespeichert in...
#   sys.__stdin__
#   sys.__stdout__
#   sys.__stderr__

# version -> wie hexversion -> nur als String
# zum Vergleichen nicht geeignet
print(sys.version)

# version_info -> Tupel mit einzelnen Komponenten der Versions-
# nummer des Interpreters
print(sys.version_info)
# Zugriff auch ueber Index
print(sys.version_info[0])
print(sys.version_info.minor)

