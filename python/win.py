#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

class Base:
    def destroy(self, widget):
        #print "You clicked the close button"
        gtk.main_quit()

    def hide(self, widget):
        self.button1.hide()

    def show(self, widget):
        self.button1.show()

    def relabel(self, widget):
        self.label1.set_text("foooooo!")

    def textchange(self, widget, button):
        button1 = self.button
        #foo = button
        #self.window.set_title("The text has been changed")
        #self.label1.set_text(self.textbox.get_text())
        self.button1.set_label(self.textbox.get_text())

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_size_request(400, 300)
        self.window.set_title("BrazosTweaker V1.0.7")

        self.button1 = gtk.Button("_Refresh")
        self.button1.connect("clicked", self.destroy)
        self.button1.set_tooltip_text("Refresh")

        self.button2 = gtk.Button("_Service...")
        self.button2.connect("clicked", self.hide)

        self.button3 = gtk.Button("_Apply")
        self.button3.connect("clicked", self.show)

        self.button4 = gtk.Button("relabel label")
        self.button4.connect("clicked", self.relabel)

        self.label1 = gtk.Label("Mult = 32 divided by ->")

        self.textbox = gtk.Entry()
        self.textbox.connect("changed", self.textchange, self.button1)

        self.textbox2 = gtk.Entry()
        self.textbox2.connect("changed", self.textchange, self.button2)

        self.box1 = gtk.VBox()
        self.box1.pack_start(self.button1)
        self.box1.pack_start(self.button2)
        self.box1.pack_start(self.button3)
        self.box1.pack_start(self.button4)
        self.box1.pack_start(self.label1)
        self.box1.pack_start(self.textbox)
        self.box1.pack_start(self.textbox2)

        self.window.add(self.box1)
        self.window.show_all()
        self.window.connect("destroy", self.destroy)

    def main(self):
        gtk.main()

if __name__ == '__main__':
    base = Base()
    base.main()

