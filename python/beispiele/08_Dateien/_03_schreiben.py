# -*- coding: utf-8 -*-
fobj = open("woerterbuch.txt", "r")
woerter = {}
for line in fobj:
	line = line.strip()
	zuordnung = line.split(" ")
	woerter[zuordnung[0]] = zuordnung[1]
fobj.close()
#print(woerter)
fobj1 = open("ausgabe.txt", "w")
for engl in woerter:
	fobj1.write("{0} {1}\n".format(engl, woerter[engl]))
fobj1.close()