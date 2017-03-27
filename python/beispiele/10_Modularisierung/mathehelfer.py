# -*- coding: utf-8 -*-

def fak(n):
	ergebnis = 1
	for i in range(2, n+1):
		ergebnis *= i
	return ergebnis

def kehr(n):
	return 1/n