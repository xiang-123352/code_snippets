# -*- coding: utf-8 -*-

# Nutzen von lambda bei häufigem
# Gebrauch mit voller Funktionalität

f = lambda x : x * 3 + 7

r = f(10)
print(r)

f1 = lambda x, y, z : (x - y) * z

# entspricht

def f2(x, y, z):
	return (x -y) * z

# lambda in Klammern ist Aufruf ohne
# v erherige Referenzierung

print((lambda x, y, z: (x -y) * z)(1,2,3))