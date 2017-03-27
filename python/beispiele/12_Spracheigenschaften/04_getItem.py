# -*- coding: utf-8 -*-


class Quadrate:

	def __init__(self,max_n):
		self.MaxN = max_n

	def __getitem__(self, index):
		index += 1
		if index > len(self) or index < 1:
			raise IndexError
		return index * index

	def __len__(self):
		return self.MaxN

lst = list(Quadrate(20))
print(lst)