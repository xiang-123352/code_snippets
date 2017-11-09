#!/usr/bin/python
# -*- coding: utf8 -*-

# ZetCode PyGTK tutorial 
#
# This example shows how to use
# the Table container widget
#
# author: jan bodnar
# website: zetcode.com 
# last edited: February 2009


import gtk


class PyApp(gtk.Window):

    def __init__(self):
        super(PyApp, self).__init__()

        self.set_title("BrazosTweaker V1.0.7")
        self.set_size_request(400, 300)
        self.set_position(gtk.WIN_POS_CENTER)

        vbox = gtk.VBox(False, 2)
        
        #mb = gtk.MenuBar()
        #filemenu = gtk.Menu()
        #filem = gtk.MenuItem("File")
        #filem.set_submenu(filemenu)
        #mb.append(filem)

        #vbox.pack_start(mb, False, False, 0)

        table = gtk.Table(5, 4, True)

        table.attach(gtk.Button("Cls"), 0, 1, 0, 1)
        table.attach(gtk.Button("Bck"), 1, 2, 0, 1)
        table.attach(gtk.Label(), 2, 3, 0, 1)
        table.attach(gtk.Button("Close"), 3, 4, 0, 1)

        table.attach(gtk.Button("7"), 0, 1, 1, 2)
        table.attach(gtk.Button("8"), 1, 2, 1, 2)
        table.attach(gtk.Button("9"), 2, 3, 1, 2)
        table.attach(gtk.Button("/"), 3, 4, 1, 2)

        table.attach(gtk.Button("4"), 0, 1, 2, 3)
        table.attach(gtk.Button("5"), 1, 2, 2, 3)
        table.attach(gtk.Button("6"), 2, 3, 2, 3)
        table.attach(gtk.Button("*"), 3, 4, 2, 3)

        table.attach(gtk.Button("1"), 0, 1, 3, 4)
        table.attach(gtk.Button("2"), 1, 2, 3, 4)
        table.attach(gtk.Button("3"), 2, 3, 3, 4)
        table.attach(gtk.Button("-"), 3, 4, 3, 4)

        table.attach(gtk.Button("0"), 0, 1, 4, 5)
        table.attach(gtk.Button("."), 1, 2, 4, 5)
        table.attach(gtk.Button("="), 2, 3, 4, 5)
        table.attach(gtk.Button("+"), 3, 4, 4, 5)

        moo = gtk.Entry()
        moo.set_text("APU: 55°C MoBo: 40°C Fan: 1450 RPM")

        vbox.pack_start(moo, False, False, 0)
        vbox.pack_end(table, True, True, 0)

        self.add(vbox)

        self.connect("destroy", gtk.main_quit)
        self.show_all()
        

PyApp()
gtk.main()

