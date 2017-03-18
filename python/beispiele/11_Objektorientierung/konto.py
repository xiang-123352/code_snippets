# -*- coding: utf-8 -*-


class Konto:
	def __init__(self, inhaber, kontonummer, kontostand, max_tagesumsatz = 1500):
		self.Inhaber = inhaber
		self.Kontonummer = kontonummer
		self.Kontostand = kontostand
		self.MaxTagesumsatz = max_tagesumsatz
		self.UmsatzHeute = 0

	def einzahlen(self, betrag):
		if(betrag < 0 or self.UmsatzHeute + betrag > self.MaxTagesumsatz):
			return False
		else:
			self.Kontostand += betrag
			self.UmsatzHeute += betrag
			return True

	def auszahlen(self, betrag):
		if(betrag < 0 or self.UmsatzHeute + betrag > self.MaxTagesumsatz):
			return False
		else:
			self.Kontostand -= betrag
			self.UmsatzHeute += betrag
			return True

	def geldtransfer(self, ziel, betrag):
		if(betrag < 0 or self.UmsatzHeute + betrag > self.MaxTagesumsatz or ziel.UmsatzHeute + betrag > ziel.MaxTagesumsatz):
			return False
		else:
			self.Kontostand -= betrag
			self.UmsatzHeute += betrag
			ziel.Kontostand += betrag
			ziel.UmsatzHeute += betrag
			return True

	def zeige(self):
		print("Konto von {0}".format(self.Inhaber))
		print("Aktueller Kontostand: {0:.2f} Euro".format(self.Kontostand))
		print("(Heute schon {0:.2f} von {1:.2f} Euro umgesetzt)".format(self.UmsatzHeute, self.MaxTagesumsatz))