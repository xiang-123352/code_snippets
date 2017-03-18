# -*- coding: utf-8 -*-

class GirokontoKundendaten:

	def __init__(self, inhaber, kontonummer):
		self.Inhaber = inhaber
		self.Kontonummer = kontonummer

	def zeige(self):
		print("Inhaber:", self.Inhaber)
		print("Kontonummer:", self.Kontonummer)