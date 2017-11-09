#!/usr/bin/python2
# -*- coding: utf-8 -*-

from Xlib import X, display, error
import time

disp = display.Display()
root = disp.screen().root
root.change_attributes(event_mask=X.SubstructureNotifyMask)

def getProp(win, prop):
    p = win.get_full_property(disp.intern_atom('_NET_WM_' + prop), 0)
    return [None] if (p is None) else p.value

while True:
    event = disp.next_event()
    if event.type == X.CreateNotify:
        newWin = event.window
        try:
            newWinName = getProp(newWin, 'NAME')
            newWinPID = getProp(newWin, 'PID')[0]

            if newWinName and newWinPID:
                print time.strftime('%H:%M:%S'), "- new window:", newWinPID, newWinName
            else:
                print 'NAME or PID property not found.'
            print

        except Xlib.error.BadWindow:
            print "BadWindow error"
