# -*- coding: utf-8 -*-

# exec kann jeglichen Code auswerten
# und das Ergebnis zurücgeben

#print("Definieren Sie eine Funktion mit 1 Parameter.")
#definition = input()
#kontext = {"pi" : 3.14159}
#exec(definition,kontext)
#for i in range(5):
#	print("f({0}) = {1}".format(i, kontext['f'](i)))


# Ausfruecke auswerten mit eval
# eval(source[,globals[,locals]])
print(eval("5 * 4"))
x = 10
print(eval("5 * x"))

# Kontext = leeres Dictionary
print(eval("5 * x", {}))