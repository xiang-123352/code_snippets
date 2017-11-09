#!/usr/bin/env python
'''
FILE:        pyrun.py
REQUIRES:    PyGTK >= 2.0, python
DESCRIPTION: Basic pygtk run dialog box
              Version 0.2
CREATOR:     Andrew Gwozdziewycz <gwozdzie@lucas.cis.temple.edu>
LICENSE:     GPL <http://www.gnu.org/licenses/gpl.txt>

CHANGELOG
Oct 1, 2004:
   - History
     * Fixed bug which didn't include in history full paths

Sept 22, 2004:
   - History
     * Fixed bug which put last entry last instead of first 
     * Deleted duplicate history entries
     
Aug 9, 2004:
   - Changed entry box to combo box (using deprecated gtk.Combo() for now
     * PyGTK 2.4 uses new construct and deprecates gtk.Combo()
     * need to work out handling all of them... 
   - Added history

'''

import gtk
import sys
import os
import string

HIST_FILE = os.getenv('HOME') + '/' + '.pyrunhistory'
HIST_SIZE = 7

class PyRun:
   'implments a simple run dialog box'
   def delete_event(self, widget, event, data=None):
      return gtk.FALSE

   def destroy(self, widget, data=None):
      gtk.main_quit()

   def __init__(self):
      self.history = []
      self.window = gtk.Window()
      self.label = gtk.Label("Run...")
      self.window.connect("delete_event", self.delete_event)
      self.window.connect("destroy", self.destroy)
      self.window.set_border_width(10)
      self.window.set_title("Run...")
      self.button = gtk.Button("Launch")
      self.button.connect("clicked", self.run_it)
      self.cancel = gtk.Button("Cancel")
      self.cancel.connect("clicked", self.destroy)
      self.combo = gtk.Combo()
      self.combo.entry.set_text('')
      self.combo.set_size_request(200, 25)
      self.combo.entry.connect("activate", self.run_it)
      self.history = self.read_history()
      self.combo.set_popdown_strings(self.history)
      topbox = gtk.HBox(gtk.FALSE, 0)
      botbox = gtk.HBox(gtk.FALSE, 0)
      fullbox = gtk.VBox(gtk.FALSE, 0)
      topbox.pack_start(self.label, gtk.FALSE, gtk.FALSE, 0)
      botbox.pack_start(self.combo, gtk.FALSE, gtk.FALSE, 0)
      botbox.pack_start(self.button, gtk.FALSE, gtk.FALSE, 0)
      botbox.pack_start(self.cancel, gtk.FALSE, gtk.FALSE, 0)
      fullbox.pack_start(topbox, gtk.FALSE, gtk.FALSE, 0)
      fullbox.pack_start(botbox, gtk.FALSE, gtk.FALSE, 0)
      self.combo.show()
      self.button.show()
      self.cancel.show()
      self.label.show()
      topbox.show()
      botbox.show()
      fullbox.show()
      self.window.add(fullbox)
      self.window.show()

   def read_history(self):
       ''' Read the history file '''
       lis = []
       try:
           hisin = open(HIST_FILE)
           lin = hisin.readlines()
           lin.reverse()
           hisin.close()
           for n in lin:
               n = n.replace('\n', '')
               lis.append(n)
           print lis
       except IOError:
           lis.append('')
           pass
       return lis

   def write_history(self, newentry):
      if len(self.history) > HIST_SIZE:
         self.history = self.history[1:]
      self.history.reverse()
      if newentry in self.history:
         self.history.remove(newentry)
      self.history.append(newentry)
      lines = []
      for n in self.history:
          if n != '':
            print n
            lines.append(n + '\n' )

      if len(lines) > HIST_SIZE:
         lines = lines[1:]

      try:
          hisfile = open(HIST_FILE, 'w')
          hisfile.writelines(lines)
          hisfile.close()
      except IOError:
          sys.stderr.write('pyrun: Couldn\'t write history file\n')

   def run_it(self, data=None):
      '''
       finds the location of the command to be run and calls launch on success
       and not_found on failure
      '''
      # call os.execlp (does PATH for us)
      command_line = self.combo.entry.get_text().strip()
      args = command_line.split(' ')
      if string.find(args[0], '/') != -1: # must be a path... 
        if os.path.exists(args[0]): # if it exists, just run it...
          self.write_history(command_line)
          self.launch(args[0], args)
        else:
          self.not_found(args[0]) # this is our error handling, 
      else:  # not a path, see if its in our path...
        program_path = self.find_exec(args[0])
        if program_path == None:
          self.not_found(args[0]) # couldn't find the file we needed
        else:
          self.write_history(command_line)
          self.launch(program_path, args)

   def not_found(self, data=None):
      'shows a file not found dialog box and exits program when button clicked'
      dialog = gtk.Dialog('File not found', self.window, gtk.DIALOG_DESTROY_WITH_PARENT)
      dbutton = gtk.Button("Ok")
      dbutton.connect("clicked", self.destroy)
      dbutton.show()
      dlabel = gtk.Label("File not found!")
      dlabel.show()
      dialog.action_area.pack_start(dbutton, gtk.FALSE, gtk.FALSE, 0)
      dialog.vbox.pack_start(dlabel, gtk.FALSE, gtk.FALSE, 0)
      dialog.show()

   def find_exec(self, data):
      'finds the full path of the executable to run'
      path = os.environ.get('PATH')
      for n in string.split(path, os.pathsep):
         if os.path.exists(n + '/' + data):
           return n + '/' + data
      return None

   def launch(self, exe, args):
      'forks, execs, parent exits'
      print 'launching %s with args %s' % (exe, args)
      pid = os.fork()
      if pid == 0:
        os.execv(exe, args)
      elif pid < 0:
        print "Couldn't fork, exiting"
        os._exit(0) 
      else:
        self.destroy(self.window)
        gtk.main_quit()

def main():
   gtk.main()
   return 0

if __name__ == '__main__':
   runbox = PyRun()
   main()

      
