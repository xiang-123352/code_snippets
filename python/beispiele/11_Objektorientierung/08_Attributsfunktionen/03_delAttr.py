# -*- coding: utf-8 -*-


# delattr(object, name)
# entspricht -> del object.name
class C:
	
	def __init__(self):
		for i in range(10):
			setattr(self, "X{}".format(i), i)

c = C()
print(c.X4)
delattr(c, "X4")
print(c.X4)