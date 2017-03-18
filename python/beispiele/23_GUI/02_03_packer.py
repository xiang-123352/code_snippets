# -*- coding: utf-8 -*-

"""
Es ist moeglich alles von Hand zu definieren, aber
macht man nicht.
Position, Groesse und Verhalten.

Packer -> Anordnung der Steuerelement im Dialog
Programmierer -> Vorgabe zur Ausrichtung
"""

# Hierarchische Anordnung
# ALLE Kindelemente werden an Vaterelement gehangen und soweiter
# Kapseln sinnvoll, da man so alles in einem Rutsch machen kann
# Frame-Widget wirdhaeufig verwendet

from tkinter import *
def zeigeBild():
    root = Tk()
    logo = PhotoImage(file=r"tkinter/hierarchie.png")
    w = Label(root, image=logo).pack(side="top")
    root.mainloop()
 
#zeigeBild()
   
def mehrBilder():
    root = Tk()
    logo1 = PhotoImage(file=r"tkinter/bild1.png")
    logo2 = PhotoImage(file=r"tkinter/bild2.png")
    logo3 = PhotoImage(file=r"tkinter/bild3.png")
    w1 = Label(root, image=logo1).pack(side="top")
    w2 = Label(root, image=logo2).pack()
    w3 = Label(root, image=logo3).pack()
    root.mainloop()
    
#mehrBilder()

# Der Packer arbeitet immer ein einem viereckigen Bereich
# Widget erzeugen:
# Wenn man keine Layout-Angaben macht, nutzt er 100% Breite
# und ist immer nach oben ausgerichtet
# Arbeitsbereich wird kleiner um Groesse des Widgets/Buttons

def paramBilder():
    root = Tk()
    logo = PhotoImage(file=r"tkinter/packer_param.png")
    w = Label(root, image=logo).pack()
    root.mainloop()

#paramBilder()

# Padding -> innen und aussen (CSS -> padding und margin)
    # padding aussen -> pack(padx, pady) in px (Abstand zu anderem Widget)
    # padding innen  -> pack(ipadx, ipady) Abstand innerhalb eines Widgets

def zeigePadding():
    root = Tk()
    var = StringVar()
    var.set("Hallo")
    txt = Label(root, textvariable=var)
    txt.pack(padx=100, pady= 50)
    root.mainloop()  

zeigePadding()

# fill und expand
# Verhalten bei Vergroessern des Fensters
    # ohne Angaben -> Alle Elemente bleiben in der Mitte untereinander &
    # mit derselben Groesse wie vorher

    # fill=both -> freier Platz wird zugewiesen (leer)
    # Ausrichtung bleibt bestehen (side="right")

    # expand=True ->Elemente werden horizontal und vertikal zentriert

    # fill=both und expand=True
    # Elemente werden auf 100% Breite und Höhe des Fensters angepasst
    # Button nur Breite