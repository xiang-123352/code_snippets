# -*- coding: utf-8 -*-

import shutil

# make_archive(base_name, format[, root_dir[, base_dir[, verbose[, dry_run[,
# owner[, group[, logger]]]]]]]))
# Erzeugt ein neues Archiv, das die Dateien aus root_dir enthaelt
# Bei nicht angeben wird das aktuelle Verzeichnis gepackt
# base_name -> Speicherort des Archivs -> Dateiendung wird nicht angegeben
# format -> Angabe Speicherformat
# get_archive_formats -> benutzbare
#print(shutil.make_archive("test", "zip", "D:\Bilder"))
# Unterordner kommasepariert nach root_dir

# get_archive_formats -> Lister mit Tupeln
print(shutil.get_archive_formats())

# get_unpack_formats()

# unpack_archive(filename[,extract_dir[,format]])
# entpackt ARchiv unter filename nach extract_dir
# ohne Angabe Format -> versuch anhand der Endung automatisch zu entpacken

print(shutil.unpack_archive("test.zip", "./Unpack", "zip"))