#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Person:
    def __init__(self, name, vorname, alter):
        self.name = name
        self.vorname = vorname
        self.alter = alter

    def getName(self):
        return self.name

    def getVorname(self):
        return self.vorname

    def getAlter(self):
        return self.alter

    def __str__(self):
        return "Name: " + self.name + ", Vorname: " + self.vorname + ", Alter: " + self.alter

    def __eq__(self, other):
        if id(other) == id(self):       # Wenn id gleich, dann alles andere auch gleich, dann True
            return True
        if other == None:               # Wenn übergebenes Objekt 'None', dann False
            return False
        if type(other) != type(self):   # Wenn type ungleich, dann False
            return False
        if other.getName() == self.name and other.getVorname() == self.vorname and other.getAlter() == self.alter:
            return True


    def __hash__(self):
        x = 17
        value = 1
        value = x * value + (0 if self.name == None else self.name.__hash__())
        value = x * value + (0 if self.vorname == None else self.vorname.__hash__())
        value = x * value + (0 if self.alter == None else self.alter.__hash__())
        return value


p1 = Person("Anderson", "Thomas", "42")
p2 = Person("Anderson", "Thomas", "42")
p3 = p1
p4 = Person("Winifred", "Klaus-Maria", "42")
print(p1)
print(p1.__hash__())
print(p2.__hash__())
print(p3.__hash__())
print(p4.__hash__())
print(id(p1))
print(id(p2))
print(id(p3))
print(id(p4))

s = set()
s.add(p4)
s.add(p3)
s.add(p2)
s.add(p1)

p4.vorname = "Thomas"
p4.name = "Anderson"

for p in s:
    print(p)

