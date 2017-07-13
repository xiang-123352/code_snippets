#!/usr/bin/env python
# coding: utf8   
""" 
This PyGtk example shows two windows, the master and his dog. 
After master window moves or changes size, the dog window moves to always stay at its right border. 
This example should also account for variable thickness of the window border.
Public domain, Filip Dominec, 2012
"""

import sys, gtk

class Main: 
    def __init__(self):
        self.window1 = gtk.Window(); self.window1.set_title("Master")
        self.window2 = gtk.Window(); self.window2.set_title("Dog")

        self.window1.connect('configure_event', self.on_window1_configure_event) # move master -> move dog
        self.window1.connect('destroy', lambda w: gtk.main_quit()) # close master -> end program

        self.window1.show_all()
        self.window2.show_all()

    def on_window1_configure_event(self, *args):
        print "Window 1 moved!"
        x, y   = self.window1.get_position()
        sx, sy = self.window1.get_size()
        tx = self.window1.get_style().xthickness
        self.window2.move(x+sx+2*tx,y)

MainInstance = Main()
gtk.main()
