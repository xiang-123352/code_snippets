# -*- coding: utf-8 -*-

# Schleifen vorzeitig verlassen

# Bedingung erweitern
# versuch != geheimnis and versuch != 0

geheimnis = 1337
versuch = 0
while versuch != geheimnis:
	versuch = int(input("Raten Sie: "))
	if versuch == 0:
		print("Spiel beendet")
		break
print("Geschafft")
