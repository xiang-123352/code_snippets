#!/usr/bin/env python

# example spinbutton.py

import pygtk
pygtk.require('2.0')
import gtk

class DurationSettings:
    def ok_cb(self,widget,data=None):
        self.hour=int(self.spinner_hour.get_value())
        self.minute=int(self.spinner_minute.get_value())
        self.second=int(self.spinner_second.get_value())
        self.window.hide()

    def initialize(self):
        self.hour=0
        self.minute=0
        self.second=0

    def cancel_cb(self,widget,data=None):
        self.initialize()
        self.window.hide()

    def show(self):
        self.window.show_all()

    def __init__(self):
        self.initialize()
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("destroy", lambda w: gtk.main_quit())
        self.window.set_title("Caffeine")

        main_vbox = gtk.VBox(False, 5)
        main_vbox.set_border_width(10)
        self.window.add(main_vbox)

        frame = gtk.Frame("Duration")
        main_vbox.pack_start(frame, True, True, 0)
  
        vbox = gtk.VBox(False, 0)
        vbox.set_border_width(5)
        frame.add(vbox)
        hbox = gtk.HBox(False, 0)
        vbox.pack_start(hbox, True, True, 5)
  
        vbox2 = gtk.VBox(False, 0)
        hbox.pack_start(vbox2, True, True, 5)

        label = gtk.Label("Hours:")
        label.set_alignment(0, 0.5)
        vbox2.pack_start(label, False, True, 0)
  
        adj = gtk.Adjustment(0.0, 0.0, 99.0, 1.0, 5.0, 0.0)
        self.spinner_hour = gtk.SpinButton(adj, 0, 0)
        self.spinner_hour.set_wrap(True)
        vbox2.pack_start(self.spinner_hour, False, True, 0)
  
        vbox2 = gtk.VBox(False, 0)
        hbox.pack_start(vbox2, True, True, 5)
  
        label = gtk.Label("Minutes:")
        label.set_alignment(0, 0.5)
        vbox2.pack_start(label, False, True, 0)

        adj = gtk.Adjustment(0.0, 0.0, 59.0, 1.0, 5.0, 0.0)
        self.spinner_minute = gtk.SpinButton(adj, 0, 0)
        self.spinner_minute.set_wrap(True)
        vbox2.pack_start(self.spinner_minute, False, True, 0)
  
        vbox2 = gtk.VBox(False, 0)
        hbox.pack_start(vbox2, True, True, 5)
  
        label = gtk.Label("Seconds:")
        label.set_alignment(0, 0.5)
        vbox2.pack_start(label, False, True, 0)
  
        adj = gtk.Adjustment(0.0, 0.0, 59.0, 1.0, 100.0, 0.0)
        self.spinner_second = gtk.SpinButton(adj, 0, 0)
        self.spinner_second.set_wrap(True)
        self.spinner_second.set_size_request(55, -1)
        vbox2.pack_start(self.spinner_second, False, True, 0)
  
        hbox = gtk.HBox(False, 0)
        main_vbox.pack_start(hbox, False, True, 0)

        button = gtk.Button(stock="OK")
        button.connect("clicked", self.ok_cb)
        hbox.pack_start(button, True, True, 5)
        button = gtk.Button(stock="Cancel")
        button.connect("clicked", self.cancel_cb)
        hbox.pack_start(button, True, True, 5)


class MainWin:

    def destroy(self, widget, data=None):
        print "destroy signal occurred"
        gtk.main_quit()

    def duration_cb(self, widget, data=None):
        self.ds.show()

    def report_cb(self,widget,data=None):
        print('%02i:%02i:%02i'%(self.ds.hour,self.ds.minute,self.ds.second))

    def __init__(self):
        self.ds=DurationSettings()      
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(10)
        self.hbox=gtk.HBox(homogeneous=False,spacing=0)
        self.window.add(self.hbox)
        self.button_duration=gtk.Button('Set Duration')
        self.button_duration.connect('clicked', self.duration_cb)
        self.button_report=gtk.Button('Report')
        self.button_report.connect('clicked', self.report_cb)
        self.hbox.pack_end(self.button_duration)
        self.hbox.pack_end(self.button_report)
        self.button_duration.show()
        self.button_report.show()
        self.hbox.show()
        self.window.show()

    def main(self):
        gtk.main()

if __name__ == "__main__":
    MainWin().main()

