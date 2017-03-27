# -*- coding: utf-8 -*-
#d = {"k1":"v1", "k2":"v2", "k3":"v3"}
#print(d)

# Reihenfolge unbekannt
#e = d.copy()
#print(e)

#d.clear()
#print(d)

### Bereich II ###
### Dictionary wird kopiert
### Aber die Inhalte sind Referenzen
### Hier auf dieselbe Liste
#d1 = {"key" : [1,2,3]}
#d2 = d1.copy()
#d2["key"].append(4)
#print(d2)
#print(d1)
#print(d1["key"] is d2["key"])

### Bereich III ###
#d = {"k1":"v1", "k2":"v2", "k3":"v3"}
#print(d.get("k2", 1234))
#print(d.get("k5", 1234))

# K-V-Pairs
#for paar in d.items():
#	print(paar)

# Keys
#for key in d.keys():
#	print(key)

#for key in d:
#	print(key)

#print(list(d.keys()))

### Bereich IV ###
# Holen und Entfernen
#d = {"k1":"v1", "k2":"v2", "k3":"v3"}
#print(d.pop("k1"))
#print(d.pop("k3"))
#print(d)
#print(d.popitem())
#print(d)
#d.setdefault("k2", 1234)
#d.setdefault("k5", 1234)
#print(d)
#d.update({"k4" : "v4"})
#print(d)
#d.update({"k1" : "Python RockZ"})
#print(d)

### VALUES ###
#d = {"k1":"v1", "k2":"v2", "k3":"v3"}
#for v in d.values():
#	print(v)

# Class dict -> static method fromkeys
# erzeugt ein neues dictionary
#dfk = dict.fromkeys([1,2,3], "Python")
dfk = dict.fromkeys([1,2,3])
print(dfk)