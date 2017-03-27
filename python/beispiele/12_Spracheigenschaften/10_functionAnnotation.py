# -*- coding: utf-8 -*-


""" def funktion(p1: Annotation, p2: Annotation) -> Annotation3:
	Funktionskoerper
	
	Dem Interpreter sind Annotations egal
	
	Alle Annotations werden in einem Dictionary gespeichert
	funktion.__annotations__ =  {
                                		"p1" : Annotation1,
                                		"p2" : Annotation2,
                                		
                                		"return" : Annotation3
                                  }"""


# Gut fuer Typueberpruefung an der Schnittstelle
# Funktion soll n mal den String str wiedergeben
def strmult(s: str, n: int) -> str:
	return s*n

# Solche Funktionen (komplett durch Anno's beschrieben) koennen nur
# mit call-Funktion gerufen werden
def call(f, **kwargs):
    for arg in kwargs:
        if arg not in f.__annotations__:
            raise TypeError("Parameter '{0}' unbekannt".format(arg))
        if not isinstance(kwargs[arg], f.__annotations__[arg]):
            raise TypeError("Parameter '{0}' hat ungültigen Typ".format(arg))
    ret = f(**kwargs)
    if type(ret) != f.__annotations__["return"]:
        raise TypeError("Ungültiges Rückgabewert")
    return ret
 
 # Aufruf
#print(call(strmult, s="Hallo", n=3))

# fehlerhaft
#print(call(strmult, s="Hallo", n="Welt))
print(call(strmult, s=13, n=3))