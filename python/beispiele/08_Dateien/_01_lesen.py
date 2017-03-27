# -*- coding: utf-8 -*-
fobj = open("woerterbuch.txt", "r")
#for line in fobj:
#	print(line)
#fonj.close()

#woerter = {}
#for line in fobj:
#	zuordnung = line.split(" ")
#	woerter[zuordnung[0]] = zuordnung[1]
#fobj.close()
#print(woerter)

woerter = {}
for line in fobj:
	line = line.strip()
	zuordnung = line.split(" ")
	woerter[zuordnung[0]] = zuordnung[1]
fobj.close()
print(woerter)