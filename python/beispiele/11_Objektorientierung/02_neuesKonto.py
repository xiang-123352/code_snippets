# -*- coding: utf-8 -*-

# Funktion fuer neues Konto
def neues_konto(inhaber, kontonummer,kontostand, max_tagesumsatz=1500):
	return {
		"Inhaber" : inhaber,
		"Kontonummer" : kontonummer,
		"Kontostand" : kontostand,
		"MaxTagesumsatz" : max_tagesumsatz,
		"UmsatzHeute" : 0
		}

# Ueberweisung
# Quelle, Ziel, Betrag
def geldtransfer(quelle, ziel, betrag):
	#Test ob Transfer moeglich
	if(betrag < 0 or
	quelle["UmsatzHeute"] + betrag > quelle["MaxTagesumsatz"] or
	ziel["UmsatzHeute"] + betrag > ziel["MaxTagesumsatz"]):
		#Transfer unmoeglich
		return False
	else:
		#Alles ok
		quelle["Kontostand"] -= betrag
		quelle["UmsatzHeute"] += betrag
		ziel["Kontostand"] += betrag
		ziel["UmsatzHeute"] += betrag
		return True

#Einzahlung
def einzahlen(konto, betrag):
	if (betrag < 0 or konto["UmsatzHeute"] + betrag > konto["MaxTagesumsatz"]):
		#Limit erreicht
		return False
	else:
		konto["Kontostand"] += betrag
		konto["MaxTagesumsatz"] += betrag
		return True

#Auszahlung
def auszahlen(konto, betrag):
	if (betrag < 0 or konto["UmsatzHeute"] + betrag > konto["MaxTagesumsatz"]):
		#Limit erreicht
		return False
	else:
		konto["Kontostand"] -= betrag
		konto["UmsatzHeute"] += betrag
		return True

#Kontostand
#Einzahlung
def zeige_konto(konto):
	print("Konto von {0}".format(konto["Inhaber"]))
	print("Aktueller Kontostand: {0:.2f} Euro".format(konto["Kontostand"]))
	print("Heute schon {0:.2f} von {1} Euro umgesetzt".format(konto["UmsatzHeute"], konto["MaxTagesumsatz"]))

# Objekte erzeugen
k1 = neues_konto("Gyula Orosz", 123456, 1200.0)
k2 = neues_konto("Jürgen Pauli", 987654, 1800.0)
#zeige_konto(k1)
#zeige_konto(k2)
geldtransfer(k2,k1,200)
zeige_konto(k1)
zeige_konto(k2)