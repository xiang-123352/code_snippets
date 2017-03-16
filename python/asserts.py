
class Irgend:
    def was(self, text):
        print("was? " + text)
        return 2

    def _private(self, anderes):
        assert type(anderes) == type("b")
        print("privates -> " + anderes)
        assert type(anderes) == type("b")
        return "bla: " + anderes


i = Irgend()
anderes = "öffentlich"

assert type(anderes) == type("b")
res = i.was(anderes)
assert res == 2

i._private("text")


x = 1
y = 11
z = 2

assert x >= 0
for i in range(x, y, z):
    print(i)


def mach_was(wasn):
    print("Mach was: " + wasn)

wert = "2"
print(type(wert))
mach_was(wert)