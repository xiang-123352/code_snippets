# -*- coding: utf-8 -*-

def func(a, b):
	print("Id der Instanz in der Funktion", id(a))
	print("Id der Instanz in der Funktion", id(b))

#p = 1
#q = [1,2,3]
#print("Id der Instanz", id(p))
#print("Id der Instanz", id(q))
#print(func(p, q))

# Unsichere Listen
def func1(liste):
	liste[0] = 42
	liste += [5,6,7,8,9]

#zahlen = [1,2,3,4]
#print(zahlen)
#print(func1(zahlen))
#print(zahlen)

def func2(a=[1,2,3]):
	a += [4,5]
	print(a)

func2()
func2()
func2()
func2()

# IMMUTABLE None -> Save
def func3(a=None):
	if a is None:
		a = [1,2,3]
	print(a)

func3()
func3()
func3()
func3()