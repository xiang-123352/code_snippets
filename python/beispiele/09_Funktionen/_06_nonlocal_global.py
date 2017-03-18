# -*- coding: utf-8 -*-

# Es gibt mehrer Arten der ineinander veschachtelten
# Funktionen

def f1():
	global s
	s = "lokaler String"
	print(s)

s = "globaler String"
f1()
print(s)

# Anderer Weg ist nonlocal
# Geht ueber alle Verschachtelungsebenen

def f2():
	
	def f_i1():
		nonlocal res
		res += 1
	
	res = 1
	f_i1()
	print(res)

f2()