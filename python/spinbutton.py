#!/usr/bin/env python

import gtk

def scale_output(scale, value):
    if value < 0:
        return "Infinity"  # u"\u221E"
    return "{0}".format(int(value))

window = gtk.Window(gtk.WINDOW_TOPLEVEL)
adjustment = gtk.Adjustment(-1, -1, 100, 1, 1)
scale = gtk.HScale(adjustment)
window.set_default_size(300, 100)
window.add(scale)
scale.connect('format-value', scale_output)
window.connect('destroy', gtk.main_quit)
window.show_all()
gtk.main()

