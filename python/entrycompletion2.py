#!/usr/bin/env python

import gtk

class Application:
    def __init__(self):
        window = gtk.Window()
        window.set_title = "My gtk.EntryCompletion"
        #window.set_window_position = gtk.WindowPosition.CENTER
        #window.connect("destroy", gtk.main_quit())
        window.set_default_size (350, 70)

        #  The Entry:
        entry = gtk.Entry()

        #  The EntryCompletion:
        completion = gtk.EntryCompletion()
        #completion.set_completion(completion)

        #  Create, fill & register a ListStore:
        list_store = gtk.ListStore (str)
        completion.set_model (list_store)
        completion.set_text_column (0)

        iter = GtkTreeIter

        #list_store.append (out iter)
        list_store.set (iter, 0, "Burgenland")
        #list_store.append (out iter)
        list_store.set (iter, 0, "Carinthia")
        #list_store.append (out iter)
        list_store.set (iter, 0, "Lower Austria")
        #list_store.append (out iter)
        list_store.set (iter, 0, "Upper Austria")
        #list_store.append (out iter)
        list_store.set (iter, 0, "Salzburg")
        #list_store.append (out iter)
        list_store.set (iter, 0, "Styria")
        #list_store.append (out iter)
        list_store.set (iter, 0, "Tyrol")
        #list_store.append (out iter)
        list_store.set (iter, 0, "Vorarlberg")
        #list_store.append (out iter)
        list_store.set (iter, 0, "Vienna")

app = Application ()

app.show_all ()

gtk.main ()

