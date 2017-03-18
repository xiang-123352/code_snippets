# -*- coding: utf-8 -*-

import AllgemeinesKonto as ak


class AllgemeinesKontoMitTagesumsatz(ak.AllgemeinesKonto):

	def __init__(self, kundendaten, kontostand, max_tagesumsatz=1500):
		ak.AllgemeinesKonto.__init__(self, kundendaten, kontostand)
		self.MaxTagesumsatz = max_tagesumsatz
		self.UmsatzHeute = 0.0

	def transferMoeglich(self, betrag):
		return (self.UmsatzHeute + betrag <= self.MaxTagesumsatz)

	def auszahlenMoeglich(self, betrag):
		return self.transferMoeglich(betrag)

	def einzahlenMoeglich(self, betrag):
		return self.transferMoeglich(betrag)

	def einzahlen(self, betrag):
		if ak.AllgemeinesKonto.einzahlen(self, betrag):
			self.UmsatzHeute += betrag
			return True
		else:
			return False

	def auszahlen(self, betrag):
		if ak.AllgemeinesKonto.auszahlen(self, betrag):
			self.UmsatzHeute += betrag
			return True
		else:
			return False

	def zeige(self):
		ak.AllgemeinesKonto.zeige(self)
		print("Heute schon {:.2f} von {:.2f} Euro umgesetzt".format(self.UmsatzHeute, self.MaxTagesumsatz))