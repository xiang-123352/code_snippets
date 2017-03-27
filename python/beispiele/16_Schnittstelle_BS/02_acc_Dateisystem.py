# -*- coding: utf-8 -*-

"""
Mit den hier stehenden Funktionen kann man sich die das Dateisystem
wie mit einem Dateimanager oder einer Shell bewegen,
Informationen zu Dateien und Ordnern ermitteln,
diese umbenennen, erstellen oder loeschen

Oft Nutzung von Pfad als Parameter (absolut oder relativ)
"""

import os

# access(path, mode) -> prueft welche Rechte das laufende P-Prog
# fuer den Pfad path hat
# mode -> Bitmaske, der zu ueberpruefenden Rechte (einzeln oder |)
# True, wenn alle für mode übergebenen Werte auf den Pfad zutreffen
# False, wenn mindestens ein Zugriffsrecht für das Programm nicht gilt.
#   F_OK -> Pfad existent
#   R_OK -> Pfad lesbar
#   W_OK -> Pfad schreibbar
#   X_OK -> Pfad ausfuehrbar
print(os.access("C:\\Python34\\python.exe", os.F_OK | os.X_OK))
# Alles ok. Interpreter ist da und ist ausfuehrbar

#chomd(path, mode) 1 = x, 2 = w, 4 = r
#os.chmod("test.txt", 0o400)
#f = open("test.txt", "w")
#for z in f:
#   print(z)
# PermissionError: [Errno 13] Permission denied: 'test.txt'

# listdir(path)
# Liste aller Dateien und Unterordner von path (nicht "." oder "..")
# Elemente der Liste haben denselben Typ wie path (str oder bytes)
#print(os.listdir("D:\Kurse"))

# mkdir(path[,mode])
# Legt einen neuen Ordner in path an
# mode = Bitmaske 0o777
# Wenn vorhanden dann OSError
# Geht nur, wenn alle Ueber-Ordner vorhanden sind, sonst WindowsError
#pfad = os.environ['HOMEDRIVE'] + os.environ['HOMEPATH'];
#print(os.mkdir(r""+ pfad  + "\Desktop\Test"))

# Abilfe makedirs(path[,mode])
#print(os.makedirs(r"D:\Das\ist\neu\Test"))

# remove(path) -> Fuer Datei loeschen (Ordner geht nicht -> os.error)

# removedirs(path) ->Loescht Ordnerstruktur#
# Rueckwaerts -> Test -> neu -> ist -> Das
# Verschachtelt nicht leere Verzeichnisse loescht man mit
# shutil.rmtree()
#print(os.removedirs(r"D:\Das\ist\neu\Test"))

# rename(src, dst)- > Benennt Ordner/Datei src in dst um
# Falls schon vorhanden ->OSError
# Bei Unix OSError nur bei Ordner -> Datei wird ueberschrieben
# Klappt nur, wenn Ordnerstruktur von dst existiert

# Fuer Verzeichnisse -> renames(src, dst)

# walk(top[,topdown=True[,onerror=None]])
# Java -> walkFileTree
# walk durchlauft alles innerhalb von "top"
# Gibt ein Tuple mit 3 Elementen zu Unterordner zurueck
# Elem1 = relativer Pfad zu top
# Elem2 = Liste mit allen Ordnern des Unterordners
# Elem3 = speichert alle Dateien desUnterordners

for t in os.walk("D:\Bilder"):
    print(t)

# Normal beim obersten Element
# Bei topdown=False -> Beginnt walk in der untersten Ebene

for t in os.walk("D:\Bilder", False):
    print(t)

# Bei onerror != None muss eine Funktion referenziert werden,
# die einen Parameter (Beschreibung) entgegen nimmt(Instanz von os.error)