# -*- coding: utf-8 -*-

import GirokontoMitTagesumsatz as gmt

k1 = gmt.GirokontoMitTagesumsatz("Gyula Orosz", 123456789, 15000.0)
k2 = gmt.GirokontoMitTagesumsatz("Jürgen CP", 987654321, 19000.0)

k1.zeige()
k2.zeige()

k1.geldtransfer(k2, 160)
k2.geldtransfer(k1,1000)
k2.geldtransfer(k1,500)
k2.einzahlen(500)

k1.zeige()
k2.zeige()