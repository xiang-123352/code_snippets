#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Demo Programm um die verschiedenen Möglichkeiten einer GUI
in Python 3 mit tk zu ermitteln 
"""
import tkinter,tkinter.ttk
 
# Methoden um die verschiedenen Events zu händeln
def local_exit():
    mainWindow.destroy()
def local_changeColor():
    pass
 
def local_changeProperty():
    label1checkBox1["text"]=str(property1.get())
 
def local_convertText():
    pass
 
def local_readFile():
    filename = tkinter.filedialog.askopenfilename(parent=mainWindow,title='Wähle eine Datei aus')
    inputTextFeldMulti.insert("end",filename)
 
def local_pressKey(e):
    label2TField["text"] = "Zeichen: " + e.char
 
def local_showListbox():
    label1listBox1["text"]=listBox1.get("active")
 
def local_getRBValue():
    label1radioButton3["text"]=color.get()
 
def local_showScale(self):
    label1scale1["text"]=scaleValue.get()
 
def local_readComboBox(self):
    label1combobox1["text"]=boxValue.get()
 
#Mouse handling
def local_mMove(e):
    labelImage2["text"]= "x::"+str(e.x)+" y::"+str(e.y)
def local_mLinks(e):
    labelImage2["text"]= "Mouse Right on x::"+str(e.x)+" y::"+str(e.y)
def local_mRechts(e):
    labelImage2["text"]= "Mouse Left on xx::"+str(e.x)+" y::"+str(e.y)
    # zeige auf dem Bild ein Context Menü an
    gm = mainWindow.geometry()
    #Position im Context des Hauptfensters - nicht ideal....
    #Fix it
    positionen = gm.split("+")
    contextMenuFarbe.tk_popup(int(positionen[1]) + 60 + e.x + 8, int(positionen[2]) + 30 + e.y + 30)
 
# Messages Boxen anzeigen
 
def local_MessageInfo():
    tkinter.messagebox.showinfo("Info", "Eine Information")
 
def local_MessageWarning():
    tkinter.messagebox.showwarning("Warnung", "Eine Warnung")
 
def local_MessageError():
    tkinter.messagebox.showerror("Fehler", "Ein Fehler")
 
def local_MessageYesNo():
    antwort = tkinter.messagebox.askyesno("Ja/Nein", "Ja oder Nein")
    if antwort == 1:
        tkinter.messagebox.showinfo("Ja", "Positiv")
    else:
        tkinter.messagebox.showinfo("Nein", "Negativ")
 
def local_MessageQuestion():
    antwort = tkinter.messagebox.Message(mainWindow
                                         ,type=tkinter.messagebox.ABORTRETRYIGNORE
                                         ,icon=tkinter.messagebox.QUESTION
                                         ,title="Abbrechen + Wiederholen + Ignorieren"
                                         ,message="Suchen Sie sich etwas aus").show()    
    if   antwort == "abort":
        tkinter.messagebox.showinfo("Antwort", "Abbrechen")
    elif antwort == "retry":
        tkinter.messagebox.showinfo("Antwort", "Wiederholen")
    else:
        tkinter.messagebox.showinfo("Antwort", "Ignorieren")
 
 
#Hauptfenster erzeugen
mainWindow=tkinter.Tk()
mainWindow.title("Demo Programm TK Python")
 
#--------------------------------------
#Statusbar einfügen
 
#Für eine Statusbar muss ein eigenes Fenster eingeführt werden
#in das Fenster wird dann später das das Grid Layout eingefügt
#pack und grid layout können nicht gemischt werden!
#
 
winMain =tkinter.Frame(mainWindow)
winMain.pack()
winMain.grid_columnconfigure(0, weight=1)
winMain.grid_rowconfigure(1, weight=1)
 
#Satus Bar anlegen
statusBar = tkinter.Label(mainWindow, text="", bd=1, relief=tkinter.SUNKEN, anchor=tkinter.W)
# so nur wenn kein Grid Layout
statusBar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
#statusBar.grid(row=0,column=0,sticky="we")
 
 
#--------------------------------------
#Menüleiste zum Hauptfenster hinzufügen
 
#Menü erzeugen
mBar=tkinter.Menu(mainWindow)
#Eine Menü Liste mit normalen Einträgen erstellen
mFile=tkinter.Menu(mBar)
 
#Menü Elemente einfügen
mFile.add_command(label="Neu"       , underline=0)
mFile.add_command(label="Speichern" , underline=0)
mFile.add_separator()
mFile.add_command(label="Beenden"  ,command=local_exit ,underline=0)
 
# Dem Hauptmenü diese Liste hinzufügen
mBar.add_cascade(label="Datei",menu=mFile, underline=0)
 
#Eine Menü Liste mit Checkbox/Radio Button Verhalten erstellen
#widget Variablem zum Speichern der Auswahlwerte
color= tkinter.StringVar()
color.set("#FF0000")
property1 = tkinter.IntVar()
property1.set(0)
 
#Neues Menüliste
mView=tkinter.Menu(mBar)
mView.add_radiobutton(label="Rot"  ,variable=color ,value="#FF0000" ,underline=0 ,command=local_changeColor)
mView.add_radiobutton(label="Gelb" ,variable=color ,value="#00FF00" ,underline=0 ,command=local_changeColor)
mView.add_radiobutton(label="Blau" ,variable=color ,value="#0000FF" ,underline=0 ,command=local_changeColor)
mView.add_separator()
mView.add_checkbutton(label="Eigenschaft A setzen", variable=property1, onvalue=1, offvalue=0, underline=5,command=local_changeProperty)
 
# Dem Hauptmenü diese Liste hinzufügen
mBar.add_cascade(label="Ansicht",menu=mView, underline=0)
 
#Dem Hauptfenster das gesamte Menü zuordnen
mainWindow["menu"]= mBar
#
#--------------------------------------
 
 
#--------------------------------------
#
# 6 Frames für die Aufnahme der möglichen Elemente erzeugen
# Diese Frames mit einem Grid Layout so anordnen
# |1|2|3
# |4|5|6
# |7|8|9
 
frame1=tkinter.Frame(winMain,width=200,height=100,relief="ridge",bd=1)
frame1.grid(row=0,column=0)
frame2=tkinter.Frame(winMain,width=200,height=100,relief="ridge",bd=1)
frame2.grid(row=0,column=1)
frame3=tkinter.Frame(winMain,width=200,height=100,relief="ridge",bd=1)
frame3.grid(row=0,column=2)
frame4=tkinter.Frame(winMain,width=200,height=100,relief="ridge",bd=1)
frame4.grid(row=1,column=0)
frame5=tkinter.Frame(winMain,width=200,height=100,relief="ridge",bd=1)
frame5.grid(row=1,column=1)
frame6=tkinter.Frame(winMain,width=200,height=100,relief="ridge",bd=1)
frame6.grid(row=1,column=2)
 
frame7=tkinter.Frame(winMain,width=200,height=100,relief="ridge",bd=1)
frame7.grid(row=2,column=0)
frame8=tkinter.Frame(winMain,width=200,height=100,relief="ridge",bd=1)
frame8.grid(row=2,column=1)
frame9=tkinter.Frame(winMain,width=200,height=100,relief="ridge",bd=1)
frame9.grid(row=2,column=2)
 
 
 
#--------------------------------------
#
# Text Eingabe Feld in Frame 1 mit Button
# 
 
 
#Label neben dem Textfeld erzeugen
labelTField=tkinter.Label(frame1,text="Text:1")
labelTField.grid(row=0,column=0)
 
inputTField=tkinter.Entry(frame1)
# Gesamten Platz in der zweiten Spalte ausfüllen
inputTField.grid(row=0,column=1,sticky="we")
 
 
#Button unter dem Text Feld
but1TField=tkinter.Button(frame1,text="Convert Text",command=local_convertText)
#Mittig unter den beiden Elementen
but1TField.grid(row=1,column=0,columnspan=2)
 
#Tastatur auf das Textfild binden
inputTField.bind("<X>", local_pressKey)
inputTField.bind("<x>", local_pressKey)
inputTField.bind("<Y>", local_pressKey)
inputTField.bind("<y>", local_pressKey)
 
 
#Label unter dem Textfeld erzeugen
label2TField=tkinter.Label(frame1,text="-------")
label2TField.grid(row=3,column=0,columnspan=2,sticky="we")
#
#--------------------------------------
# Bild in Frame 2 anzeigen
# Maus Position über dem Bild anzeigen
# Einfach in den Frame mit pack hinzufügen
 
#Image einbinden
labelImage1=tkinter.Label(frame2)
#Referenz auf eine Bilddatei
image1=tkinter.PhotoImage(file="d:\wiki\mandelbrot_01.png")
#dabei etwas skalieren
image2=image1.subsample(5, 5)
#Bild einfügen und 
labelImage1["image"]=image2
labelImage1.pack()
 
#Unter dem Bild ein Label einfügen
labelImage2=tkinter.Label(frame2,text="maus über den Bild bewegen")
labelImage2.pack()
 
 
#Bewegung der Maus einbinden
labelImage1.bind("<Motion>"   ,local_mMove)
labelImage1.bind("<Button 1>" ,local_mLinks)
labelImage1.bind("<Button 3>" ,local_mRechts)
# <Control-Button 1>
# <Alt-Button 1>
# <ButtonRelease 1>
# <Enter>
# <Leave>
 
# Kontext Menü auf dem Bild
contextMenuFarbe = tkinter.Menu(frame2)
contextMenuFarbe.add_radiobutton(label="Rot"    , variable=color, value="#FF0000", command=local_getRBValue)
contextMenuFarbe.add_radiobutton(label="Gelb"   , variable=color, value="#FFFF00", command=local_getRBValue)
contextMenuFarbe.add_radiobutton(label="Schwarz", variable=color, value="#000000", command=local_getRBValue)
 
#
#--------------------------------------
# Mehrzeiliges Textfeld  mit Scrollbar
 
#Scrollbar vorab definieren
scrollbarTextFeld1=tkinter.Scrollbar(frame4,orient="vertical")
 
#Mehrzeiliges Textfeld
inputTextFeldMulti=tkinter.Text(frame4,width=30,height=10,yscrollcommand=scrollbarTextFeld1.set)
 
inputTextFeldMulti.pack(side="left")
scrollbarTextFeld1.pack(side="left",fill="y")
 
#Scrollbar mit dem Textfeld verbinden
scrollbarTextFeld1.config(command=inputTextFeldMulti.yview)
 
#testdaten einfügen
for t in range(30):
    inputTextFeldMulti.insert("end","Wert::"+str(t)+"\n")
 
#Mit dem Text arbeiten
but1TFieldMulti=tkinter.Button(frame4,text="Einlesen \n mit File Open",command=local_readFile)
but1TFieldMulti.pack(side="top")
 
#
#--------------------------------------
#
# List Box zur Auswahl eines Elementes 
# mit einer Scrollbar
scrollbarListBox1=tkinter.Scrollbar(frame5,orient="vertical")
 
#Falls height=0 größer nach Anzahl Elemente
#und mit der Scrollbar verknüpfen
listBox1=tkinter.Listbox(frame5,height=10,yscrollcommand=scrollbarListBox1.set)
 
#Scrollbar mit der Listbox verknüpfen
scrollbarListBox1["command"] = listBox1.yview
 
#Werte hinterlegen
for i in range(30):
    listBox1.insert("end","Wert ::"+str(i))
 
#Mit der Scrollbar zusammen anzeigen
listBox1.pack(side="left")
scrollbarListBox1.pack(side="left",fill="y")
 
 
#Listbox auswerten
but1listBox1=tkinter.Button(frame5)
but1listBox1.configure(text="Liste auswerten",command=local_showListbox)
but1listBox1.pack()
label1listBox1=tkinter.Label(frame5,text="Listen Auswahl")
label1listBox1.pack(side="bottom")
#
#--------------------------------------
#
# Radio Butto
#
 
# Gemeinsame widget Variable für die Radiobuttons
# wird von der Variablen color (siehe Menü Bereich verwendet!)
 
#Button erstellen
radioButton1=tkinter.Radiobutton(frame3, text="rot" ,variable=color,  value="#FF0000",command=local_getRBValue)
radioButton1.pack()
radioButton2=tkinter.Radiobutton(frame3, text="gelb" ,variable=color, value="#00FF00",command=local_getRBValue)
radioButton2.pack()
radioButton3=tkinter.Radiobutton(frame3, text="blau" ,variable=color, value="#0000FF",command=local_getRBValue)
radioButton3.pack()
 
#Gewählten Werte anzeigen
label1radioButton3=tkinter.Label(frame3,text=color.get())
label1radioButton3.pack()
but1radioButton3=tkinter.Button(frame3,text="RB Auswahl",command=local_getRBValue)
but1radioButton3.pack()
 
#
#--------------------------------------
# Seperator anzeigen
 
#Fix it - not visible??
 
sep1=tkinter.ttk.Separator(frame3,orient="horizontal")
sep1.pack()
 
#
#--------------------------------------
# Check Boxen 
 
# Gemeinsame widget Variable für die CheckBox
# wird von der Variablen property1 (siehe Menü Bereich verwendet!)
 
#Checkbox
checkBox1=tkinter.Checkbutton(frame3,text="Auswahl"
                              ,variable=property1
                              ,onvalue=1
                              ,offvalue=0
                              ,command=local_changeProperty)
 
checkBox1.pack()
 
#Checkbox Wert anzeigen
label1checkBox1=tkinter.Label(frame3,text=property1.get(),width=20)
label1checkBox1.pack()
 
#
#--------------------------------------
#
# Schieberegler 
 
# Widget Variable
scaleValue=tkinter.IntVar()
scaleValue.set(0)
 
scale1=tkinter.Scale(frame6
                     ,width=20
                     ,length=200
                     ,orient="horizontal"
                     ,from_=0
                     ,to=100
                     ,resolution=2
                     ,tickinterval=10
                     ,command=local_showScale
                     ,variable=scaleValue)
scale1.pack()
 
# Werte von Scale anzeigen
label1scale1=tkinter.Label(frame6,text=scaleValue.get(),width=20)
label1scale1.pack()
 
#
#--------------------------------------
#
# Message Boxem aufrufen
 
but1MessageBox=tkinter.Button(frame7,text="Eine Information",command=local_MessageInfo)
but1MessageBox.pack()
 
but2MessageBox=tkinter.Button(frame7,text="Eine Warnung ausgeben",command=local_MessageWarning)
but2MessageBox.pack()
 
but3MessageBox=tkinter.Button(frame7,text="Einen Fehler anzeigen",command=local_MessageError)
but3MessageBox.pack()
 
but4MessageBox=tkinter.Button(frame7,text="Eine Frage mit 3 Optionen stellen",command=local_MessageQuestion)
but4MessageBox.pack()
 
but4MessageBox=tkinter.Button(frame7,text="Ja/Nein Eine Frage stellen",command=local_MessageYesNo)
but4MessageBox.pack()
#
#--------------------------------------
#
treeView = tkinter.ttk.Treeview(frame9)
 
treeView["columns"]=("one","two")
treeView.column("one", width=100 )
treeView.column("two", width=100)
treeView.heading("one", text="coulmn A")
treeView.heading("two", text="column B")
 
treeView.insert("" , 0,    text="Line 1", values=("1A","1b"))
 
id2 = treeView.insert("", 1, "dir2", text="Dir 2")
treeView.insert(id2, "end", "dir 2", text="sub dir 2", values=("2A","2B"))
 
##alternatively:
treeView.insert("", 3, "dir3", text="Dir 3")
treeView.insert("dir3", 3, text=" sub dir 3",values=("3A"," 3B"))
 
treeView.pack()
 
#
#--------------------------------------
#
# Combo Box
 
boxValue = tkinter.StringVar()
 
#Box anlegen
combobox1 = tkinter.ttk.Combobox(frame8
                                 , textvariable=boxValue
                                 , state='readwrite')
 
#Werte hinzufügen
combobox1['values'] = ('A', 'B', 'C')
#Aktuelle Auswahl setzen
combobox1.current(0)
 
#
#Style
#
#Eigenschaften ändern
style = tkinter.ttk.Style()
style.configure("GPI.TCombobox", foreground="red")
 
#Setzen
combobox1.configure(style="GPI.TCombobox")
 
 
#Auslesen verknüpfen
combobox1.bind('<<ComboboxSelected>>', local_readComboBox)
 
#
# Falls ein neuer Wert eingeben wurde, diese mit in die Liste aufnehmen
#
def local_update_values(evt):
        newValue = combobox1.get()          # get current text
        allVals = combobox1.cget('values')  # get values         
        if not allVals:
            combobox1.configure(values = (newValue, ))
        elif newValue not in allVals:
            combobox1.configure(values = allVals + (newValue, ))
        label1combobox1["text"]=newValue    
 
#Events binden
combobox1.bind('<Return>', local_update_values)
combobox1.bind('<Tab>', local_update_values)
 
 
combobox1.pack()
 
 
# Werte von der ComboBox anzeigen
label1combobox1=tkinter.Label(frame8
                              , text=boxValue.get()
                              , width=20)
label1combobox1.pack()
 
 
#
#--------------------------------------
#
# Progress bar
 
progressBar = tkinter.ttk.Progressbar(frame8
                                      , orient='horizontal'
                                      , length=200
                                      , mode='determinate')
 
 
progressBar.pack(side="bottom", fill="both")
 
progressBar['value'] = 500
progressBar['maximum'] = 1000
 
def local_updateSatus():
    if progressBar['value'] < 1000:
        progressBar['value'] += 20
    else:
        progressBar['value']=0
 
but1progressBar=tkinter.Button(frame8,text="Update Progress",command=local_updateSatus)
but1progressBar.pack()        
 
#
#-------------------------------------
#
# Table from the treeview element
#treeTableView = tkinter.ttk.Treeview(frame1)
 
#treeTableView["columns"]=("A","B","C","D")
#treeTableView.column("A", width=20 )
#treeTableView.column("B", width=20 )
#treeTableView.column("C", width=20 )
#treeTableView.column("D", width=20 )
 
#treeTableView.heading("A", text="Col A")
#treeTableView.heading("B", text="Col B")
#treeTableView.heading("C", text="Col C")
#treeTableView.heading("D", text="Col D")
 
#treeTableView.insert("" , 0,    text="1", values=("1","2","3","4"))
#treeTableView.insert("" , 0,    text="2", values=("1","2","3","4"))
#treeTableView.insert("" , 0,    text="3", values=("1","2","3","4"))
#treeTableView.insert("" , 0,    text="4", values=("1","2","3","4"))
#treeTableView.insert("" , 0,    text="5", values=("1","2","3","4"))
 
#treeTableView.grid(row=2,column=0,columnspan=2)
#
#-------------------------------------
#
 
 
#Starte das Hauptfenster
mainWindow.mainloop()
