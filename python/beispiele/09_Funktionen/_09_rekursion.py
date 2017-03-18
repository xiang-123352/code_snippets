# -*- coding: utf-8 -*-

def fak(n):
	if n > 0:
		return fak(n - 1) * n
	else:
		return 1

print(fak(6))