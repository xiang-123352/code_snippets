# -*- coding: utf-8 -*-

"""
Das ist eine Ergaenzung zu os und os.path
Abstrakte Funktionen um besonders Kopieren und Entfernen
BS-unabhaengig zu nutzen

Ab 3.2 auch zum Packen und Entpacken (zip und tar)
"""

# copyfileobj(fsrc,fdst[,length])
# Kopiert den Inhalt lesend von fsrc zu schreibend fdst
# length -> Zwischenspeichergroesse
#   wenn pos -> Happenweise Lesen und danach happenweise schreiben
#   wenn neg -> fsrc wird komplett gelesen und danach komplett in
#   fdst geschrieben

# copy(src,dst)
# Kopiert die Datei unter Pfad src nach dst
# Datei in dst kann erzeugt oder ueberschrieben werden
# akzeptiert auch einen Ordner als dst (Datei wird dann erzeugt)
# Zugriffsrechte werden mitkopiert

# copytree(src,dst,symlinks=False,ignore=None,copy_function=copy2,
#          ignore_dangling_symlinks=False)
# kopiert die gesamte Ordnerstruktur von src nach dst
# Der Pfad unter dst darf noch nicht existieren
# symlinks = True -> Nur Links werden kopiert
# Falls ignore=False && ignore_dangling_symlinks=True
# = Fehler(falsche Links) werden ignoriert
# ignore erwartet Funktionen, die bestimte Dateien aussschliesst
# ignore_patterns
# my_ignore_function = shutil.ignore_patterns("*.txt", "tmp*")
# copy durch Funktion hinter copy_function
# intern copy_stat fuer Rechte-Copy

# rmtree(src[,ignore_errors[,onerror]])
# Verzeichnisstruktur unter src wird geloescht
# ignore_errors -> klar
# onerror -> Angabe einer Funktion mit 3 Parameter
#   Referenz auf Funktionk, die den Fehler verursacht
#   path, wo der Fehler auftrat
#   excinfo -> Rueckgabewert von sys.exc_info im Kontext des Fehlers

