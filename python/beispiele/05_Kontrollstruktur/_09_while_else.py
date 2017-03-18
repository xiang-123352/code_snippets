# -*- coding: utf-8 -*-

# Unterscheidung fehlt, ob es geschafft wurde oder
# ob das Spiel beendet wurde
# SONDERFALL
# In Python kann man Schleifen mit einem else-Fall
# versehen

geheimnis = 1234
versuch = 0
while versuch != geheimnis:
	versuch = int(input("Raten Sie: "))
	if versuch > geheimnis:
		print("zu gross")
	if versuch < geheimnis:
		print("zu klein")
	if versuch == 0:
		print("Spiel beendet")
		break
else:
	print("Geschafft")