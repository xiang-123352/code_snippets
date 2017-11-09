#!/usr/bin/python -tt
#
# easy-entry application

import os, sys
from gi.repository import Gtk

class UI:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(os.path.join(os.getcwd(), 'easy-entry.ui'))
        self.window = self.builder.get_object('dialog1')
        self.close_button = self.builder.get_object('close_button')
        self.print_button = self.builder.get_object('print_button')
        self.entry = self.builder.get_object('entry')
        
        self.window.connect('delete-event', self.quit)
        self.print_button.connect('clicked', self.print_text)
        self.close_button.connect('clicked', self.quit)
        self.window.show()
    
    def print_text(self, *args):
        print '%s' % (self.entry.get_text())
    
    def quit(self, *args):
        Gtk.main_quit()

if __name__ == '__main__':
    ui = UI()
    Gtk.main()

