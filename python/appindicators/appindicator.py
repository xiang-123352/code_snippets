#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This code is an example for a tutorial on Ubuntu Unity/Gnome AppIndicators:
#
# http://candidtim.github.io/appindicator/2014/09/13/ubuntu-appindicator-step-by-step.html

import os
import signal

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository.Gdk import ScrollDirection

class AppIndicatorIcon:
    def __init__(self, appindicator_id, appindicator_icon):
        self.appindicator_id = appindicator_id
        self.appindicator_icon = appindicator_icon

        self.indicator = appindicator.Indicator.new(self.appindicator_id, os.path.abspath(self.appindicator_icon), appindicator.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.build_menu())

    def build_menu(self):
        self.menu = gtk.Menu()
        
        self.item_quit = gtk.MenuItem("Quit")
        self.item_quit.connect("activate", self.quit) # left-click on a menu item
        self.item_quit.connect("select", self.quit) # "hover" over a menu item
        self.menu.append(self.item_quit)
        
        self.indicator.set_secondary_activate_target(self.item_quit) # middle-click on indicator
        self.indicator.connect("scroll-event", self.scroll) # scroll over indicator

        self.menu.show_all()
        
        return self.menu

    def scroll(self, *args):
        scroll_direction = args[2]

        if scroll_direction == ScrollDirection.UP:
            pass
        elif scroll_direction == ScrollDirection.DOWN: # BUG: https://gitlab.gnome.org/GNOME/pygobject/issues/74
            pass

    def quit(self, *args):
        gtk.main_quit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app_indicator = AppIndicatorIcon("myappindicator", "sample_icon.svg")

    gtk.main()
