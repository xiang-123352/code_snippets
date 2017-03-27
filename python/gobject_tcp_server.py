#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import gobject
import socket

def server(host, port):
    '''Initialize server and start listening.'''

    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(1)

    print("Listening...")

    gobject.io_add_watch(sock, gobject.IO_IN, listener)

def listener(sock, *args):
    '''Asynchronous connection listener. Starts a handler for each connection.'''

    conn, addr = sock.accept()

    print("Connected")

    gobject.io_add_watch(conn, gobject.IO_IN, handler)

    return True

def handler(conn, *args):
    '''Asynchronous connection handler. Processes each line from the socket.'''

    line = conn.recv(4096)

    if line:
        print(line)

        return True
    else:
        print("Connection closed.")

        return False

if __name__=='__main__':
    ip = ''
    port = 8080

    server(ip, port)

    gobject.MainLoop().run()
