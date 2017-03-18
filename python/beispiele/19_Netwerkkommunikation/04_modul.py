# -*- coding: utf-8 -*-

import socket

# create_connection(address[,timout[,source_address]])
# Socket-Obj -> address zu source_address
    # s = socket.create_connection((ip1,port1), timeout, (ip2, port2))
    # ist damit äquivalent zu:
    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.settimeout(timeout)
    # s.bind((ip2, port2))
    # s.connect((ip1, port1))

# kann auch mit with benutzt werden
    # with socket.create_connection(("ip", port)) as s:
    # s.send(b"Hallo Welt")

print(socket.gethostbyname_ex("www.google.de"))

# getservbyname(service[,protocol])
# http||ftp && tcp||udp
print(socket.getservbyname("ftp", "tcp"))

#socket([family[, type[, proto]]])
# erzeugt neuen Socket
# family -> socket.AF_INET IPv4|| socket.AF_INET6 IPv6
# type -> socket.SOCK_STREAM TCP || socket.SOCK_DGRAM UDP

# getdefaulttimeout()
# setdefaulttimeout(timeout)
# Gleitkommazahl = max. Anzahl Sekunden, die recv auf eingehendes Paket wartet