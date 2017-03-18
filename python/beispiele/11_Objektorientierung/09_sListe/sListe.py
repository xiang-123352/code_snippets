# -*- coding: utf-8 -*-


class SortierteListe(list):


	def __init__(self, *args, **kwargs):
		list.__init__(self, *args, **kwargs)
		self.sort()


	def __setitem__(self, key, value):
		list.__setitem__(self, key, value)
		self.sort()


	def append(self, value):
		list.append(self, value)
		self.sort()


	def extend(self, sequence):
		list.extend(self, sequence)
		self.sort()


	def insert(self, i , x):
		list.insert(self, i, x)
		self.sort()


	def reverse(self):
		pass


	def __iadd__(self, s):
		erg = list.__iadd__(self, s)
		self. sort()
		return erg


def __imul__(self, n):
	erg = list.__imul__(self, n)
	self.sort()
	return erg


L = SortierteListe([6,4,3])
print(L)
L.append(2)
print(L)
L.extend([67,0,-56])
print(L)
L += [100,5]
print(L)
L *= 2
print(L)