# -*- coding: utf-8 -*-


class Fibonacci:
	def __init__(self, max_n):
		self.MaxN = max_n
		self.N = 0
		self.A = 0
		self.B = 0
	def __iter__(self):
		self.N = 0
		self.A = 0
		self.B = 1
		return self
	def __next__(self):
		if self.N < self.MaxN:
			self.N += 1
			self.A, self.B = self.B, self.A + self.B
			return self.A
		else:
			raise StopIteration


#for f in Fibonacci(10):
#	print(f, end=" ")

print(list(Fibonacci(10)))
print(sum(Fibonacci(10)))

fibu = Fibonacci(5)
for f1 in fibu:
	for f2 in fibu:
		print(f1,f2, end=", ")
	print()