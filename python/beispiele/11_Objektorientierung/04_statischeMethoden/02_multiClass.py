# -*- coding: utf-8 -*-


class A:
	def m(cls):
		print("Ich bin", cls)
	m = classmethod(m)


class B(A):
	pass


class C(A):
	pass


A.m()
a = A()
b = B()
c = C()
a.m()
b.m()
c.m()