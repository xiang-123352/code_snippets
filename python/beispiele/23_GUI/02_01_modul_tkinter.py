# -*- coding: utf-8 -*-

"""
Wurde fuer Sprache TCL Tool Command Language entwickelt
Einzige in Python enthaltene Toolkit (Standardbibliothek)
Gui nutzbar ohne zusaetzliches Laden von Libs
IDLE -> ist eine tkinter Anwendung
"""

# Beispiel Dialogfenster mit Namenseingabe
# und Namens-Spiegel

import tkinter

# Klasse erbt von tkinter.Frame
class MyApp(tkinter.Frame):

    def __init__(self, master=None):
        # Kostruktor Basisklasse
        tkinter.Frame.__init__(self, master)
        
        # Grosse festlegen
        master.minsize(width=300, height=200)
        master.maxsize(width=600, height=400)
        
        # Widget wird beim Packer angemeldet
        # Elemente werden durch Packer dynamisch ermittelt
        # und positioniert (nicht statisch durch Koordinaten)
        self.pack()
        
        # Initialisierung der Steuerelemente
        self.createWidgets()

    def createWidgets(self):
        
        # Instanz tkinter.Entry -> Eingabefeld
        self.nameEntry = tkinter.Entry(self)
        self.nameEntry.pack()        
        # Variable, die den Namen auslesen || aendern soll
        self.name = tkinter.StringVar()        
        # Platzhalter (initial Wert)
        self.name.set("Ihr Name...")        
        # Steuerelementvariable anmelden beim Entry-Widget
        # Wie bei einem Dictionary -> Schluessel "textvariable" beschreiben
        self.nameEntry["textvariable"] = self.name
        
        # Dasselbe wie bei Eingabefeld
        self.ok = tkinter.Button(self)
        self.ok["text"] = "Ok"        
        # Funktionszuweisung -> Beenden
        self.ok["command"] = root.destroy        
        # Positionswunsch
        self.ok.pack(side="right")
        
        # Siehe oben
        self.rev = tkinter.Button(self)
        self.rev["text"] = "Umdrehen"
        self.rev["command"] = self.onReverse
        self.rev.pack(side="right")
    
    def onReverse(self):
        # Umdrehen des Namens        
        self.name.set(self.name.get()[::-1])

# Instanz von tkinter erzeugen
root = tkinter.Tk()
# Instanz unserer Klasse erzeugen -> Vaterinstanz = tkinter-Instanz
app = MyApp(root)
# Anzeigen Dialog & Blockierung bis Beenden
app.mainloop()