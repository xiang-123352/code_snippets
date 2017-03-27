# -*- coding: utf-8 -*-


def m():
	print("Hallo statische Methode!")


class A:
	
	m = staticmethod(m)

# Wie in Java
# Aufruf ueber den Klassennamen

A.m()