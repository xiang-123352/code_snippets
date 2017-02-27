#!/usr/bin/env python

import gtk
import pynotify

def callback(icon):
    notification.show()

pynotify.init("Some Application or Title")
notification = pynotify.Notification("Title", "body", "dialog-warning")
notification.set_urgency(pynotify.URGENCY_NORMAL)
notification.set_timeout(pynotify.EXPIRES_NEVER)

icon = gtk.status_icon_new_from_stock(gtk.STOCK_ABOUT)
icon.connect('activate', callback)
notification.attach_to_status_icon(icon)

gtk.main()
