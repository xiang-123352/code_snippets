#!/usr/bin/env python2
# -*- coding: utf-8 -*-

def event_filter(event, user_data):
        # process event
        return gtk.gdk.FILTER_CONTINUE

screen = gtk.gdk.screen_get_default()
root = screen.get_root_window()
root.set_events(gtk.gdk.SUBSTRUCTURE_MASK)
root.add_filter(event_filter)

gtk.main()
