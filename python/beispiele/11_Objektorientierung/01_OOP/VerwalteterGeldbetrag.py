# -*- coding: utf-8 -*-


class VerwalteterGeldbetrag:

	def __init__(self, anfangsbetrag):
		self.Betrag = anfangsbetrag

	def einzahlenMoeglich(self, betrag):
		return True

	def auszahlenMoeglich(self, betrag):
		return True

	def einzahlen(self, betrag):
		if betrag < 0 or not self.einzahlenMoeglich(betrag):
			return False
		else:
			self.Betrag += betrag
			return True

	def auszahlen(self, betrag):
		if betrag < 0 or not self.auszahlenMoeglich(betrag):
			return False
		else:
			self.Betrag -= betrag
			return True

	def zeige(self):
		print("Betrag: {:.2f}".format(self.Betrag))