#!/usr/bin/env python

import gtk

class Win (gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self)
        self.set_title("Close to tray")
        self.connect("delete-event", self.delete_event)
        #create a virtical box to hold some widgets
        vbox = gtk.VBox(False)
        #make a quit button
        quitbutton = gtk.Button("Quit")
        quitbutton.connect("clicked",self.quit)
        #add the quitbutton to the vbox
        vbox.pack_start(quitbutton)
        #create a label to say *something* and add to the vbox
        label=gtk.Label("This is a test of 'close to tray' functionality")
        vbox.pack_start(label)
        #add the vbox to the Window
        self.add(vbox)
        #show all of the stuff
        self.show_all()
        #make a status icon
        self.statusicon = gtk.status_icon_new_from_stock(gtk.STOCK_GOTO_TOP)
        self.statusicon.connect('activate', self.status_clicked )
        self.statusicon.set_tooltip("the window is visible")
        #start the gtk main loop
        gtk.main()
    
    def quit(self,button):
        #quit the gtk main loop
        gtk.main_quit()
    
    def delete_event(self,window,event):
        #don't delete; hide instead
        self.hide_on_delete()
        self.statusicon.set_tooltip("the window is hidden")
        return True
        
    def status_clicked(self,status):
        #unhide the window
        self.show_all()
        self.statusicon.set_tooltip("the window is visible")
        
if __name__=="__main__":
    win = Win()

