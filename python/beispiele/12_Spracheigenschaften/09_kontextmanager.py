# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 10:06:54 2016

@author: gyula
"""

class MeinLogFile:
	
	def __init__(self, logfile):
		self.logfile = logfile
		self.f = None
	
	def eintrag(self, text):
		self.f.write("==>{0}\n".format(text))
	
	# Enter und Exit muessen implementiert werden, damit with funktioniert
	# Enter oeffnet einmal den Kontext
	# Exit schliesst diesen
	def __enter__(self):
		self.f = open(self.logfile, "w")
		return self
	
	def __exit__(self, exc_type, exc_value, traceback):
		self.f.close()

#   with MeinLogFile("logfile.txt") as log:
#       log.eintrag("Hallo Welt")
#       log.eintrag("Na, wie gehts?")

with open("logfile.txt", "r") as f:
	print(f.read())