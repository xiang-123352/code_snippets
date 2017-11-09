#!/usr/bin/python
import gtk

def get_value(widget,spin,value):
    value = "%d" % spin.get_value_as_int()
    print "value=",value
    return

def get_spin(widget):
    window = gtk.Window()
    adjustment = gtk.Adjustment(0, -90, 90, 1, 1, 1)
    spinbutton = gtk.SpinButton(adjustment,0,0)
    value = 0
    spinbutton.connect("changed",get_value,spinbutton,value)
    print "the final value is: ",value
    spinbutton.show()
    window.add(spinbutton)
    window.show()
    return

def main():
    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    window.connect("destroy", gtk.main_quit)
    window.show_all()
    table = gtk.Table(2,1,False)
    button = gtk.Button("Get Spin Value")
    button.connect("clicked",get_spin)
    table.attach(button,0,1,0,1)
    table.show()
    button.show()
    window.add(table)
    window.show_all()
    gtk.main()
    return

if __name__ == '__main__': main()

