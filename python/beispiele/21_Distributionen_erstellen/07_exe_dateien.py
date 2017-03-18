# -*- coding: utf-8 -*-

"""
Erstellen einer direkt ausfuehrbaren Datei (speziell bei Windows)

Drittanbietermodul herunterladen

http://www.cx-freeze.sourceforge.net

Modul cx_Freeze
"""
# -*- coding: utf-8 -*-

from cx_Freeze import setup, Executable

setup(
    name = "Calc.py",
    version = "1.0.0",
    description = "Einfaches Beispiel zum Thema cx_Freeze",
    author = "Gyula Orosz",
    py_modules = ["calc.py", "setup.py"],
    executables = [Executable("calc.py")]
)

# Aufruf python setup.py build