# -*- coding: utf-8 -*-

"""
Internet Message Access Protocol 4
Emails bleiben auf dem Server -> Bessere Synchronisation
Meistens werden beide Protokolle unterstützt
Mehr Kommandos...
Anlegen von Unterordner...
Hat einen Hohen Funktionsumfang
Einrichten von Mailboxen(1 Ordner pro Email)

Konstruktor: IMAP4(host[,port])
Port Standard 143
"""

import imaplib

# Jede Methode, die ein IMAP4-Kommando repraesentiert
# gibt ein Tupel zurueck (Status, [Daten])
# Status == OK || NO
# Liste von bytes-Strings oder Tupeln(Header, Daten = Antworten des Servers)
im = imaplib.IMAP4_SSL("imap.gmx.net", 993)
im.login("286270868", "hans2016")

#im.select([mailbox[, readonly]])
# Waehlt eine Mailbox aus
# Name der Mailbox und readonly==True||False
#select == Anzahl der E-Mails, die in der gewaehlten Box sind

# Es wird keine Exception geworfen, wenn die gewünschte Mailbox nicht
# existiert. Stattdessen muss der Fehler anhand des Rückgabewertes ausgemacht
# werden:
#im.select("INBOX.NichtExistent")
#('NO', [b'Mailbox does not exist, or must be subscribed to.'])

# im.list([directory[, pattern]]) -> Namen aller Mailboxen in Directory,
# die auf pattern passen
# Standard Hauptordner, alle Mailboxen(Bei nicht Angabe directory & pattern)

# im.fetch(message_set, message_parts)
# laedt Teile der Mails vom Server runter
# message_set muss ein String sein, der die Mail.ID enthaelt
# Kann "1" || "1:4" || "1:5, 7:11" || "3:*"
# message_parts -> Welche Teile sollen geladen werden
# "RFC822" -> komplette Mail inkl. Header
# (BODY[TEXT]) || (BODY[HEADER])

#im.search(charset, criterion[, ...])
# Sucht innerhalb der Mailbox nach Mails, auf die die Kriterien passen
# criterion == "ALL" || "("FROM \"Johannes\")"
#im.search(None, '(FROM "JOHANNES")')

#im.store(message_set, command, flag_list)
# modifoziert die EIgenschaften(Flags) des message_set
# command == +FLAGS(dazu) || -FLAGS(weg) || FLAGS(ersetzen)
# flag_list == "\Answered", "\Flagged", "\Deleted", "\Seen", "\Draft"

print("Viel Spass beim lösen ^^")
