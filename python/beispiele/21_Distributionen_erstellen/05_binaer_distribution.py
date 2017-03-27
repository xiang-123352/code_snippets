# -*- coding: utf-8 -*-

"""
Am wenigsten Installationsaufwand.
Mehr Arbeit fuer Developer (unterschiedliche BS -> unterschiedliche Distris)

Windows-Installer
RPM-Paket (Linux)

Trotzdem Quellcode ausliefern, da nicht alle Windows oder RPM Formate verstehen

Aufruf des Install-Scripts mit folgenden Argimenten

bdist_msi     -> MSI-Datei, der ein Modul/Paket auf Win installiert
                 dist -> Projektname-Version.win32.msi
               
bdist_rpm     -> RPM-Paket, der ein Modul/Paket auf Linix installiert
                 dist -> Projektname-Version.src.rpm

bdist_wininst -> Windows-Installer, der ein Modul/Paket auf Win installiert
                 dist -> Projektname-Version.win32.exe
                 
setup.py bdist_msi
setup.py bdist_rpm
setup.py bdist_exe
"""