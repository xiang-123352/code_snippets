# -*- coding: utf-8 -*-

import VerwalteterGeldbetrag as vg

class AllgemeinesKonto(vg.VerwalteterGeldbetrag):

	def __init__(self, kundendaten, kontostand):
		vg.VerwalteterGeldbetrag.__init__(self, kontostand)
		self.Kundendaten = kundendaten

	def geldtransfer(self, ziel, betrag):
		if (self.auszahlenMoeglich(betrag) and ziel.einzahlenMoeglich(betrag)):
			self.auszahlen(betrag)
			ziel.einzahlen(betrag)
			return True
		else:
			return False

	def zeige(self):
		self.Kundendaten.zeige()
		vg.VerwalteterGeldbetrag.zeige(self)