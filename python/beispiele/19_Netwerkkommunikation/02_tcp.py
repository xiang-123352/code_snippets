# -*- coding: utf-8 -*-

"""
Transmission Control Protocol
Keine Falsche Reihefolge oder fehlende Pakete moeglich
TXP fordert intern das Neuversenden an
"""

# Beispiel Chatprogramm
import socket

# SOCK_STREAM = TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 50000))
# Server -> passiv Modus
# Ganzzahl = max. Anzahl der zu pufferden Verbindungsversuche
s.listen(1)

try:
    while True:
        komm, addr = s.accept()
        while True:
            # Server wartet auf Nachricht
            data = komm.recv(1024)
            if not data:
                komm.close()
                break
            
            print("[{}] {}".format(addr[0], data.decode()))
            nachricht = input("Antwort: ")
            komm.send(nachricht.encode())
finally:
    s.close()