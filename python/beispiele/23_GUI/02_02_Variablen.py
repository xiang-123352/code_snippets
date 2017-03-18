# -*- coding: utf-8 -*-

"""
STEUERELEMENT-VARIABLEN

Wurden eben benutzt, ohne Erklaerung
Dienen zum Datenaustausch zwischen Programm und Oberflaeche

Eine Steuervariable ist an eine bestimmt Information eines Steuerelementes
gebunden.

z.B.
Text Eingabefeld enthaelt stets den momentan angezeigt Wert
Auf dem Weg veraenderbar
Nicht jeder Typ nutzbar -> spezielle Typen im Modul tkinter

tkinter.BooleanVar (bool)
tkinter.DoubleVar  (float)
tkinter.IntVar     (int)
tkinter.StringVar  (str)

Diese 4 erben von tkinter.Variable
"""

# Variable([master[,value[,name]]])
# Steuerelement-Variable wird erzeugt und initialisiert
    # master -> Kann ein Masterwidget sein
    # value -> Wert angebbar, den die erzeugte Instanz speichern soll
    # name -> Angabe von Name, unter dem die Variable intern (TCL-Ebene)
    # angesprochen wird. (Skriptsprache = Grundlage fuer tkinter)
    # Standard -> "PY_VARn", wobei n eine laufende Nummer
    # Dieser Parameter ist sehr speziell und sollte norm nicht benoetigt
    # benoetigt werden

# ********
# Methoden
# ********

import tkinter

# v.get() und v.set(value)
# holt b.z.w. setzt den Wert einer Variable
t = tkinter.Tk()
v = tkinter.StringVar(value="Guten Tag")
print(v.get())
v.set("Gute Nacht")
print(v.get())

"""
Hinweis:

Steuerelementvariablen koennen von mehreren Steuerelement verwendet werden.
Einfache Zusammenhaenge zwischen Inhalten verschiedener Steuerelemente
herstellbar

self.nameEntry["textvariable"] = self.name
self.rev["textvariable"] = self.name
"""