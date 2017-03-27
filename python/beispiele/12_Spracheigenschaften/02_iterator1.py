# -*- coding: utf-8 -*-


class Fibonacci2:

	def __init__(self, max_n):
		self.MaxN = max_n

	def __iter__(self):
		n = 0
		a, b = 0, 1
		for n in range(self.MaxN):
			a, b = b, a+b
			yield a


print(list(Fibonacci2(10)))
print(sum(Fibonacci2(10)))

f = Fibonacci2(5)
for f1 in f:
	for f2 in f:
		print(f1, f2, end=", ")
	print()