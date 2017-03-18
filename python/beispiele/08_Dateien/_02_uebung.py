# -*- coding: utf-8 -*-
fobj = open("woerterbuch.txt", "r")
woerter = {}
for line in fobj:
	line = line.strip()
	zuordnung = line.split(" ")
	woerter[zuordnung[0]] = zuordnung[1]
fobj.close()

while(True):
	wort = input("Geben Sie ein Wort ein: ")
	if wort in woerter.keys():
		print("Das deutsche Wort lautet:", woerter[wort])
	else:
		print("Das Wort ist unbekannt")