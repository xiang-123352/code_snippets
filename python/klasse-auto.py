#!/usr/bin/env python2
# -*- coding: iso-8859-1 -*-
class Auto:
    benzinstand=0.0    # Tankfuellung in Liter
    kilometerstand=0.0
    verbrauch=4.0      # Liter pro 100km 

    def __init__(self, verbrauch):
        print "__init__"
        print "  Auto rollt aus der Gläsernen Manufaktur"
        self.verbrauch=float(verbrauch)

    def __repr__(self):
        # Optional: Zeichenkette für str(autoobj) bzw. print autoobj
        return '<%s object verbrauch=%s l/km>' % (
            self.__class__.__name__, self.verbrauch)
    
    def tanken(self, liter):
        print "tanken"
        self.benzinstand+=liter
        print "  Benzinstand nach tanken: ", self.benzinstand, " Liter"

    def fahren(self, kilometer):
        print "fahren: Soll ", kilometer, "km fahren"
        verbrauch_fahrt=(kilometer/100)*self.verbrauch
        if self.benzinstand < verbrauch_fahrt:
            print "  So weit kann ich nicht fahren"
            print "  Benzinstand:", self.benzinstand, \
                  " Verbrauch für Fahrt:", verbrauch_fahrt
            return
        else:
            self.benzinstand-=verbrauch_fahrt
            self.kilometerstand+=kilometer
            print "  Ich bin ", kilometer, " Kilometer gefahren."
            print "  Neuer Tachostand: ", self.kilometerstand
            print "  Neuer Benzinstand: ", self.benzinstand

auto=Auto(5.0)
print auto
auto.tanken(20)
auto.tanken(20)
auto.fahren(1000)
auto.tanken(20)
auto.fahren(1000)

#  Ergebnis:
#
#  __init__
#    Auto rollt aus der Gläsernen Manufaktur
#  print --> <Auto object verbrauch=5.0 l/km>
#  tanken
#    Benzinstand nach tanken:  20.0  Liter
#  tanken
#    Benzinstand nach tanken:  40.0  Liter
#  fahren: Soll  1000 km fahren
#    So weit kann ich nicht fahren
#    Benzinstand: 40.0  Verbrauch für Fahrt: 50.0
#  tanken
#    Benzinstand nach tanken:  60.0  Liter
#  fahren: Soll  1000 km fahren
#    Ich bin  1000  Kilometer gefahren.
#    Neuer Tachostand:  1000.0
#    Neuer Benzinstand:  10.0
#
#
# [Daraus folgt: Lieber Fahrradfahren, da braucht man kein Benzin]
