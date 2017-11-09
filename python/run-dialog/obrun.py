#!/usr/bin/python

# Copyright 2005 Zaid A. <zaid.box@gmail.com>
# Distributed under the terms of the GNU General Public License v2

import os
import pygtk
pygtk.require('2.0')
import gtk

class ObRun(gtk.Window):

   def deleteEventCallback(self, widget, event, data=None):
      return False

   def okButtonCallback(self, widget, data=None):
      
      program = self.programPath.get_text()
      programArgs = program.split(' ')
      
      self.saveHistory(program)
      self.executeProgram(programArgs)
   
   def cancelButtonCallback(self, widget, data=None):
      raise SystemExit
         
   def executeProgram(self, args):
      childPID = os.fork()
      
      if childPID == 0:
         try:
            os.execvpe(args[0], args, os.environ)
         except OSError:
            errorDialog = gtk.Dialog(title="Error", parent=None, flags=gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT,
                  buttons=(gtk.STOCK_OK, gtk.RESPONSE_OK))
            errorDialog.vbox.pack_start(gtk.Label("An error has occured while trying to execute the program."),
                  expand=True, padding=15)
            errorDialog.set_default_response(gtk.RESPONSE_OK)
            errorDialog.show_all()

            if errorDialog.run() == gtk.RESPONSE_OK:
               errorDialog.destroy()
      
      if childPID != 0:
         raise SystemExit
   
   def duplicateExists(self, itemToCheck):
      for entry in self.historyList:
         for i in range(1):
            if itemToCheck == entry[i]:
               return True
      return False
   
      
   def loadHistory(self):
      
      try:
         os.stat(os.path.expanduser("~")+ "/.obrun_history")
      except OSError:
         historyFile = open(os.path.expanduser("~")+ "/.obrun_history", "w")
         historyFile.close()
            
      historyFile = open(os.path.expanduser("~")+ "/.obrun_history", "r")
      historyLines = historyFile.readlines()
      historyFile.close()
      
      entryCount = 0
      
      for entry in historyLines:
         if entryCount == self.maxHistoryEntries:
            break
         self.historyList.append([entry.strip()])
         entryCount = entryCount+1
      
   def saveHistory(self, entry):
      
      entryCount = 0
      
      historyFile = open(os.path.expanduser("~") +"/.obrun_history", "w")
      
      if self.duplicateExists(entry) == False:
         self.historyList.append([entry])
         
      for item in self.historyList:
         if entryCount == self.maxHistoryEntries:
            break
         for i in range(1):
            historyFile.write(item[i] + "\n")
         entryCount = entryCount +1

      historyFile.close()
      
   def __init__(self):
      
      gtk.Window.__init__(self, type=gtk.WINDOW_TOPLEVEL)
      
      self.set_position(gtk.WIN_POS_CENTER)
      self.set_size_request(250,90)
      self.set_border_width(5)
      self.set_title("Run application")
      
      self.connect("delete-event", self.deleteEventCallback)
      self.connect("destroy", lambda destroyCallback: gtk.main_quit())

      self.vbox = gtk.VBox()
      self.hbox = gtk.HBox()
   
      self.okButton = gtk.Button(stock=gtk.STOCK_OK)
      self.cancelButton = gtk.Button(stock=gtk.STOCK_CANCEL)
                           
      self.okButton.connect("clicked", self.okButtonCallback)
      self.cancelButton.connect("clicked", self.cancelButtonCallback)
      
      self.programPath = gtk.Entry()
      self.completionWidget = gtk.EntryCompletion()

      self.historyList = gtk.ListStore(str)
      
      self.maxHistoryEntries = 20
      self.loadHistory()
            
      self.completionWidget.set_model(self.historyList)
      self.completionWidget.set_text_column(0)
      self.programPath.set_completion(self.completionWidget)

      self.programPath.connect("activate", self.okButtonCallback)
            
      self.hbox.pack_start(self.okButton,expand=False, padding=4)
      self.hbox.pack_start(self.cancelButton, expand=False, padding=4)
            
      self.vbox.pack_start(self.programPath, expand=False, padding=5)
      self.vbox.pack_start(self.hbox, expand=False, padding=5)
         
      self.add(self.vbox)

   def main(self):
      self.show_all()
      gtk.main()

if __name__ == '__main__':
   runDialog = ObRun()
   runDialog.main()

