# -*- coding: utf-8 -*-

class A:
	
	def __init__(self):
		self.X = 1234
		print("Konstruktor von A.")

	def m(self):
		print("Methode m von A. Es ist self.X =", self.X)

class B(A):
	
	def n(self):
		print("Methode n von B")

b = B()
b.n()
b.m()