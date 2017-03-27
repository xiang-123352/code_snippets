# -*- coding: utf-8 -*-

class A:
	
	def __init__(self):
		pass

class B(A):
	
	def __init__(self):
		super(B, self).__init__()
		pass