# -*- coding: utf-8 -*-

"""
ES IST DER BESTE WEG!!!!!
BINAER-DIST FUNKTIONIERT MIT 3.4 und 3.5 NICHT RICHTIG...
NUR FREMDSOFTWARE -> DIE GEHT ABER AUCH NICHT RICHTIG

Install-Script fertig -> Erstellung Quellcode-Distribution moeglich

In das Verzeichnis des Install-Scripts gehen und aufrufen mit

setup.py sdist

Dadurch wird im Unterordner dist eine Quellcode-Distri erzeugt
nach Namensschema -> Projektname-Version.Format

Zusaetzliche Format moeglich -> --formats

setup.py sdist --formats=zip,gztar

 - zip (*.zip)
 - gztar (*.tar.gz)
 - bz2 (*.tar.bz2)
 - ztar (*.tar.Z)
 - tar (*.tar)
 
Standard:   Windows -> zip
            Unix ->    tar.gz

Alles, was im Install-Script hinterlegt wurde, wird ins dist
Verzeichnis (Archiv) aufgenommen
Zusaetzlich -> README || README.TXT automatisch mit aufgenommen,
wenn diese im Verzeichnis des Install-Scripts liegt
"""