# -*- coding: utf-8 -*-

"""
Themenfeld laesst sich in mehrere Layer (Protokollebenen) einteilen
Siehe OSI

Wichtig und unteressent ab Transportprotokolle -> TCP und UDP
TCP am meisten abstrahiert -> Most interesting

UDP, TCP, HTTP, FTP, SMTP, POP§, IMAP4, Telnet
Es gibt auch abstrakte auf UDP basierende z.B. NFS (Network File System)
Hier aber ist nur TCP interessant
"""

# Modul socket -> Socket API
# Bietet grundlegende Funktionalitaeten zur Netzwerkkommunikation
# Bildet die standatisierte Socket API.
# Idee ist, dass ein Programm Daten ueber die Netzwerkschnittstelle
# senden und empfangen kann.
# Dies muss dem BS bekannt gegeben werden, damit das Programm einen
# Socket (Steckdose) bekommt.
# Verbinsungen gehen von socket zu Socket
# egal, ob Zielrechner -> localhost, Rechner imselben net oder Internet
# IP-Adresse = String ("192.168.1.23") (8-Bit-Zahl 0 - 255)
# Pro Rechner mehrere Programme, die kommunizieren wollen -> Ports
# 16-Bit-Zahl zischen 0 und 65535
# unter 1024 dicht belegt vom System (80=HTTP, 21=FTP...)
# ab 49152 alles frei

"""
Client-Server-Systeme
Kunde-Diener-Systeme
Server ist passiv -> wartet auf Anfrage vom Clienten
Anfrage Client -> Anfrage akzeptiert ->Socket erzeugt ->Kommunikation
Serieller Server -> Kommuniktaion mit vorherigem Client abgeschlossen
-> neue Anfrage moeglich

Anderer ist paralleler und multiplexender Server

Server hat einen Verbindungssocket, an dem er lauscht
bind() und listen() binden den V-Socket an eine Netzwerkadresse
und bei Anfragen akzeptiert (accept()) -> Erzeugung Komm-Socket
send() und recv() dienen zur Komm

Sobald Komm beendet -> Komm-Objekt geloescht
Alle nicht aktuell bearbeiteten Anfragen gepuffert in Queue
Am Ende wird auch der V-Socket geschlossen

Client hat auch einen Komm-Socket -> connect()
Wenn akzeptiert -> send() und recv()

Datenuebertraugun ueber UDP oder TCP -> hier Verbindungsbehaftet = TCP
"""

import socket
# Beispiel: Client Texnachricht(UDP) -> Sever annehmen & anzeigen
# CLIENT
# Erzeugung socket-Instanz(AF_INET=Internet/IPv4, SOCK_DGRAM=UDP)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Benutzereingabe -> IP und Nachricht
ip = input("IP-Adresse: ")
nachricht = input("Nachricht: ")
# Anfrage abschicken (bytes || bytes-Array)
s.sendto(nachricht.encode(), (ip, 50000))
s.close()

# SERVER
s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    s1.bind(("", 50000))
    while True:
        daten, addr = s1.recvfrom(1024)
        print("[{}] {}".format(addr[0], daten.decode()))
finally:
    s1.close()
