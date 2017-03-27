# -*- coding: utf-8 -*-

"""Methode method wird angelegt.
Danach wird sie auf Klassenebene gezogen.
staticmethod
funktional, aber nicht sehr gut.
Besser ist die Nutzen von "Annotations"
@staticmethod

Decorator sind Notationen, die durch Hinzufuegen eine
Funktionalitaet ergaenzen.
Koennen auf Funktionen und Methoden angewandt werden.
"""
class MeineKlasse:
    
    def methode():
        pass
    
    methode = staticmethod(methode)
    
class MeineKlasse2:
    
    @staticmethod
    def methode2():
        pass

class MeineKlasse3:
    
    #@dec1
    #@dec2
    def funktion():
        pass
    
    # ist dasselbe wie
    # funktion = dec1(dec2(funktion))

# Beispiel zum Thema Cache ueber Decorator
# fuer erhebliche Geschwindigkeitsvorteile
# Da die bei einem Funktionsaufruf übergebenen Parameter als Schlüssel
# fuer das interne Cache-Dictionary verwendet werden, dürfen nur
# Instanzen hashbarer Datentypen übergeben werden.
class CacheDecorator:
    
    def __init__(self):
        self.cache = {}
        self.func = None
        
    def cachedFunc(self, *args):
        if args not in self.cache:
            self.cache[args] = self.func(*args)
            text = "Ergebnis berechnet\n"
        else:
            text = "Ergebnis geladen\n"
        return text + str(self.cache[args])
        
    def __call__(self, func):
        self.func = func
        return self.cachedFunc
        
class TestCache:    
    @CacheDecorator()
    def fak(n):
        ergebnis = 1
        for i in range(2, n + 1):
            ergebnis *= i
        return ergebnis

# Ausfuehrung
print(TestCache.fak(10))
print(TestCache.fak(15))
print(TestCache.fak(10))
print(TestCache.fak(15))