# -*- coding: utf-8 -*-

"""
POP3-Protokoll (Post Office Protocol Version 3)
USER - Username zur Auth uebertragen
PASS - Passwort zur Auth uebertragen
STAT - Statis Posteingang(z.B. neue Emails)
LIST - Informationen zu einer bestimmten Email
RETR - uebertraegt eine bestimmte Email
DELE - Loescht eine bestimmte Email
REST - Widerruft alle anstehende Loeschvorgaenge
QUIT - Beendet Pop3-Sitzung

Instanziierung - POP3(host[,port[,timeout]])
Instanz wird der Hostname des POP3-Servers uebergeben,
zwecks Verbindung
"""

import poplib

pop = poplib.POP3_SSL("pop.gmx.net", 995)
pop.user("286270868")
pop.pass_("hans2016")

# Status des Posteingangs -> 
# Tupel(Anzahl der Nachrichten, Groesse des PE)
pop.stat()

# Liste der im PE liegenden Mails
#pop.list() -> Tupel(antwort, [b"meinID laenge",...], datlen)
# auch mit Angabe der ID
#pop.list(1)

# Greift auf die Mail zu -> Tupel(antwort, zeilen, laenge)
#pop.retr(which)

# Loeschen der Mail which
#pop.dele(which)

for i in range(1, pop.stat()[0]+1):
    for zeile in pop.retr(i)[1]:
        print(zeile)
        print("***")
        
pop.quit()