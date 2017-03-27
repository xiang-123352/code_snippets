# -*- coding: utf-8 -*-

# Normaler Weg
def globale_funktion(n):
	
	def lokale_funktion(n):
		return n**2
	
	return lokale_funktion(n)

print(globale_funktion(10))

# Workaround mit vordefinierten Parametern
def globale_funktion1(n):
	
	def lokale_funktion1(n=n):
		return n**2
	
	return lokale_funktion1()

print(globale_funktion1(10))
