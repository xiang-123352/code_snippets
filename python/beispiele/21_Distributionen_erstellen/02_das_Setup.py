# -*- coding: utf-8 -*-

"""
Die Funktion Setup
"""

# distutils.core.setup(arguments) -> MUSS IN DER setup.py aufgerufen werden
# Stoesst den Installationsprozess an
# Informationen zur Distribution werden hier hinterlegt
#
# name              -> Name der Distribution

# version           -> Versionsnummer der Distribution

# description       -> kurze Beschreibeung der Distribution

# long_description  -> ausfuehrliche Beschreibung der Distribution

# author            -> Name des Autors

# author_email      -> E-Mail-Adresse des Autors

# maintainer        -> Name des Paketverwalters (Maintainer), sofern dies nicht
#                      der Autor selbst ist

# maintainer_email  -> E-Mail-Adresse des Paketverwalters

# url               -> URL einer Homepage mit weiteren Informationen zur
#                      Distribution

# download_url      -> URL fuer direkten Distributionsdownload

# packages          -> Liste von Strings, die die Namen aller Pakete enthält,
#                      die in der Distribution enthalten sein sollen

# package_dir       -> Dictionary, über das Pakete in Unterverzeichnissen in
#                      die Distribution aufgenommen werden können.

# package_data      -> Dictionary, über das Dateien, die zu einem Paket gehö-
#                      ren, mit in die Distribution aufgenommen werden können.

# py_modules        -> Liste von Strings, die die Namen aller Python-Module
#                      enthält, die in der Distribution enthalten sein sollen

# scripts           -> Liste von Strings, die die Namen aller Scriptdateien
#                      enthält, die in der Distribution enthalten sein sollen

# data_files        -> Liste von Tupeln, über die zusätzliche Dateien in die
#                      Distribution mit aufgenommen werden können.

# ext_modules       -> Liste von distutils.core.Extension-Instanzen, die die
#                      Namen aller Python-Erweiterungen enthält, die kompiliert
#                      werden und in der Distribution enthalten sein sollen.

# script_name       -> Name des Installationsscripts, das in der Distribution
#                      verwendet werden soll. Dieser Parameter ist mit
#                      sys.argv[0], also dem Namen des Scripts, vorbelegt, das
#                      gerade ausgeführt wird.

# license           -> String, Lizenz angibt, unter der die Distribution
#                      veröffentlicht wird

"""
Distribution von Paketen
************************

Wenn das Projekt aus mehreren Modulen oder mehreren Paketen besteht,
muessen/sollen die Namen aller Pakete in die Distribution aufgenommen
werden.

kw_param = packages
"""

# from distutils.core import setup

#setup(
#   [...]
#   packages = ["paket1", "paket2", "paket1.unterpaket1"]
#   )

# paket1 und paket2 -> hauptverzeichnis
# unterverzeichnis1 -> paket1

"""
manchmal gibt es einen zusetzlichen Ordner
src oder source, indem sich Module oder Pakete befinden
fuer Bekanntmachen -> package_dir von setup.py
"""

# from distutils.core import setup

#setup(
#     [...]
#     package_dir = {"" : "src"},
#     packages = ["paket1", "paket2", "paket1.unterpaket1"]
#     )

"""
Programmverzeichnis "" wird auf src gelegt
    package_dir = {"" : "src", "paket3" : "pfad/zu/meinem/paket/paket3"}

danach kann paket3 ueber packages-Liste in die Distribution aufgenommen werden
Unterpakete brauchen keinen vollen Pfad -> nur key
"""
