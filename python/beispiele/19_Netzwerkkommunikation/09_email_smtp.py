# -*- coding: utf-8 -*-

"""
Modul - Wie kommuniziert man mit einem Email-Server
Abrufen von Emails und ueber den Server Emails verschicken

Schicken: smtp-protocol -> smtplib
Abholen: pop3 || imap4-protocol  -> pop3lib || imaplib

Zum Schluss Modul email
via Mime-Coding: beliebige Dateien verschicken
"""

# smtplib (Simple Mail Transfer Protocol)
# aehnlich FTP, menschenlesbares, textbasiertes Protokoll
# Wurde um ESMTP-Standard erweiter(Extended SMTP)(Benutzer-Authentifizierung)
"""
HELO      - Start SMTP-Sizuung
EHLO      - Start ESMTP-Sitzung
MAIL FROM - Leitet Absenden ein (Absendeadresse wird beigefuegt)
RCPT TO   - Fuegt Empfaenger der Email hinzu
DATA      - Inhalt der Email angeben und abschicken
QUIT      - Beendet Sitzung (SMTP und ESMTP)

Konstruktor: SMTP([host[, port[, local_hostname[, timeout]]]])
Prot nur bei Abweichen von Port25
Domainname des lokalen Hosts(wenn nicht dann automatisch)
"""

import smtplib
s = smtplib.SMTP()
# Klasse SMTP
# Modul smtplib implementieren & Instanz(SMTP) mit Namen s
# Meistens muss s mit einem Server verbunden werden

# s.connect([host[, port]])
# Wird nur aufgerufen, wenn nicht schon eine SMTP Instanz besteht
# s.connect("smtp.test.de")

# s.login(user, password)
# s.login("Benutzername", "Passwort")

# s.sendmail(from_addr, to_addrs, msg[, mail_options[, rcpt_options]])
# SMTP-Instanz muss am SMTP-Server angemeldet sein
#Email-Adress-Format: Vorname Nachname <email@email.de>
# Empfaenger koennen auch als Liste uebergeben werden
# send(von, nach, nachricht)
# sendmail -> RV Dict -> abgewiesene Empfaenger : FehlerCode || leer

#Beispiel
print("Viel Spass beim lösen")
