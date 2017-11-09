#!/usr/bin/env python

import os
import gtk

from gtk.keysyms import Tab as KEY_TAB

home = os.environ['HOME']

with open(home + "/.bash_history") as f:
    distributions = list(f.read().splitlines())

#distributions = ["Ubuntu", "Debian", "Sabayon", "Fedora", "Arch", "Mint", "Slackware", "Mandriva", "Sidux", "Mepis"]

class EntryCompletion:
    def __init__(self):
        window = gtk.Window()
        
        liststore = gtk.ListStore(str)
        for item in distributions:
            liststore.append([item])
        
        self.completion = gtk.EntryCompletion()
        self.completion.set_inline_completion(1)
        self.completion.set_popup_completion(0)
        self.completion.set_model(liststore)
        self.completion.set_text_column(0)

        comboboxentry = gtk.Entry()
        comboboxentry.set_completion(self.completion)
        
        window.connect("destroy", lambda w: gtk.main_quit())

        window.add(comboboxentry)
        
        window.show_all()

EntryCompletion()

gtk.main()

