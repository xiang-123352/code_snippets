# -*- coding: utf-8 -*-

# Conditional Expression
# Bedingter Ausdruck

x = 2
var = (20 if x == 1 else 30)
print(var)

# A if Bedingung else B

# Beispiel
print("x hat den Wert 1" if x == 1 else "x ist ungleich 1")

# Es wir Lazy Evaluation bei der Auswertung benutzt
# Erst Bedinung pruefen und dann nur den "True-Fall"
# ausfuehren
a = 11
b = 4
xyz = (a * 2 if (a > 10 and b < 5) else b * 2)
print(xyz)