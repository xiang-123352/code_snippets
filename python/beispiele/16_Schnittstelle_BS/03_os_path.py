# -*- coding: utf-8 -*-

"""
os.path soll vor den verschiedenen BS-Namenskonventionen
und Ordnerstrukturen schuetzen
Ist eine Sammlung von BS-unabhaengigen Variablen

2 Arten der Nutzung:
    os importieren -> os.path
    os.path importieren -> path
"""

import os
import os.path as pfad

# abspath(path) -> gibt den absoluten und den normalisierten Pfad
# zurueck (siehe normpath)
print(pfad.abspath("."))

# basename(path) -> Gibt den Basisnamen des Pfades zurueck
# Der Teil hinter dem letzten Ordnertrennzeichen
# Gut fuer Herausfinden von Dateinamen
# Hier ist es wieder besser raw-Strings zu nutzen,
# da es sonst eine falsche Ausgabe gibt
print(pfad.basename(r"C:\Windows\System32\ntoskrnl.exe"))
# Fehler bei Fehlen der Datei und \
# Weglassen des \ Rueckgabe des letzten Ordnernamen
print(pfad.basename(r"C:\Windows\System32"))

# commonprefix(list) -> Gibt einen moeglischst langen String zurueck
# LCS -> Gleichheit aller String am Stueck
print(pfad.commonprefix([r"C:\Windows\System32\ntoskrnl.exe",r"C:\Windows\System\TAPI.dll",r"C:\Windows\system32\drivers"]))

# dirname(path) -> Gibt den Ordnerpfad zurueck, den path enthaelt
print(pfad.dirname(r"C:\Windows\System\TAPI.dll"))

# Genau wie bei basename -> Abweichende Pfade bei Nutzung von \ oder nicht

# exists(path) -> True, wenn auf existierende Datei/Pfad verweist

print(pfad.exists(r"C:\Windows\System32\calc.exe"))

# getatime(path) -> Gibt Unix-Timestamp von letzten Zugriff zurueck
# Nicht vorhandene Datei/Pfad oder fehlende Rechte -> OSError

# getmtime(path) -> Gibt Unix-Timestamp von letzter Manipulation zurueck
# Nicht vorhandene Datei/Pfad oder fehlende Rechte -> OSError

# join(path1[,path2[,...]])
# Verkettet die uebergebenen Pfade zu einem
# OS-abhaengiges Trennzeichen
print(pfad.join(r"C:\Windows", r"System\ntoskrnl.exe"))

# normcase(path) -> toLowerCase() -> / wird zu \
print(pfad.normcase(r"C:\Windows/System32/ntoskrnl.exe"))

# split(path) -> Gibt Tuple zurueck
# Trennt Datei von Ordner
print(pfad.split(r"C:\Windows\System32\ntoskrnl.exe"))

# Problem bei Ordner am Ende mit \
#print(pfad.split(r"C:\Windows\System32\"))

# splitdrive(path) -> Trennt Laufwerk ab -> Unix Probleme
# Rueckgabe als Tuple
print(pfad.splitdrive(r"C:\Windows\System32\ntoskrnl.exe"))

#splittext(path) -> Trennt die Endung der Datei ab
print(pfad.splitext(r"C:\Windows\System32\Notepad.exe"))