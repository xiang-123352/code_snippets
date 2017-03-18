# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 13:36:54 2016

@author: gyula
"""

import re

m = re.match(r"(P[Yy])(th.n)", "Python")
m1 = re.match(r"(P[Yy])(th.n)", "Jathon")
# m.expand(template)
# Nimm den x. Treffer(Gruppe) und Packe es in den String
print("expand")
print(m.expand("**\g<1>**"))
# print(m.group(0)) -> vollstaendig passender String
print("group(1)")
print(m.group(1))
# 'Py'
print("group(1,2)")
print(m.group(1,2))
# ('Py', 'thon' )

# Groups
# Tuple -> Defaultausgabe erstellen
# Geht NICHT MEHR!!! -> da das Match-Object nicht erzeugt wird, 
# wenn keine Uebereinstimmungen da sind
#print(m1.groups("Nix gefunden"))

#groupdict
c2 = re.compile(r"(?P<gruppe1>P[Yy])(?P<gruppe2>th.n)")
m2 = c2.match("Python")
print("groupdict")
print(m2.groupdict())
print("start(1)")
print(m2.start(1))
print("end(1)")
print(m2.end(1))
print("start(2)")
print(m2.start(2))
print("end(2)")
print(m2.end(2))