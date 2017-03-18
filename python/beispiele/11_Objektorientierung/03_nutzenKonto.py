# -*- coding: utf-8 -*-

import konto as k

kto = k.Konto("Gyula Orosz", 123456789, 19999.0)
kto1 = k.Konto("Jürgen CP", 987654321, 19999.0)

kto.zeige()
kto.zeige()
kto.einzahlen(500)
kto1.auszahlen(1000)
kto1.geldtransfer(kto, 500)
kto.auszahlen(600)
kto.zeige()
kto1.zeige()