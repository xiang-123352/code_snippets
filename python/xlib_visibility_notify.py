#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re, sys, time
import Xlib.X, Xlib.XK, Xlib.display, Xlib.protocol

def parse_action(string):
    state = {
              '0': 0,
              '1': 1,
              '2': 2,
              'unobscured': 0,
              'partiallyobscured': 1,
              'fullyobscured': 2,
              'visibilityunobscured': 0,
              'visibilitypartiallyobscured': 1,
              'visibilityfullyobscured': 2,
             }[string.lower()]
    return state

def parse_window(display, arg):
    wid = int(arg, 0)
    return display.create_resource_object('window', wid)

def send_event(display, window, state):
    window.send_event(Xlib.protocol.event.VisibilityNotify(window=window,
                                                           state=state))
    display.sync()

if __name__ == "__main__":
    display = Xlib.display.Display()
    send_event(display, parse_window(display, sys.argv[1]), parse_action(sys.argv[2]))
