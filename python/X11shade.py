#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                     Version 2, December 2004
#
#  Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>
#
#  Everyone is permitted to copy and distribute verbatim or modified
#  copies of this license document, and changing it is allowed as long
#  as the name is changed.
#
#             DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#    TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#    0. You just DO WHAT THE FUCK YOU WANT TO.

import sys
from Xlib import display, X, Xatom, Xutil
import Xlib.protocol.event

def send_event(root, win, data, type, mask):
    """send event to the root"""
    event = Xlib.protocol.event.ClientMessage(window = win, client_type = type, data = (32, (data)))
    root.send_event(event, event_mask = mask)    

class X11Shade:
    def __init__(self):
        self.display = display.Display()
        self.screen = self.display.screen()
        self.root = self.screen.root
        self._ACTIVE_WINDOW   = self.display.intern_atom('_NET_ACTIVE_WINDOW')
        self._CLIENT_LIST     = self.display.intern_atom('_NET_CLIENT_LIST')
        self._CURRENT_DESKTOP = self.display.intern_atom('_NET_CURRENT_DESKTOP')
        self._DESKTOP         = self.display.intern_atom('_NET_WM_DESKTOP')
        self._STATE           = self.display.intern_atom('_NET_WM_STATE')
        self._SHADED          = self.display.intern_atom('_NET_WM_STATE_SHADED')
        
    def run(self, action):       
        """list and shade/unshade windows on active desktop except active one"""        
        active = self.root.get_full_property(self._ACTIVE_WINDOW, 0).value[0]       
        curDesk = self.root.get_full_property(self._CURRENT_DESKTOP, 0).value[0]
        tasks = self.root.get_full_property(self._CLIENT_LIST, Xatom.WINDOW).value
        
        for task in tasks:
            win  = self.display.create_resource_object('window', task)
            name = win.get_wm_name()
            desk = win.get_full_property(self._DESKTOP, 0).value[0]
            state = win.get_full_property(self._STATE, Xatom.ATOM).value            
            if desk == curDesk:               
                if int(task) != active:
                    if action == 1:                                                
                        if not self._SHADED in state:
                            self.doShade(win)
                    else:                                                
                        if (self._SHADED in state):
                            self.doUnShade(win)

        self.display.flush()   # this magic command must be here !!!
               
    def doShade(self, win):
        """send shade event"""
        data = [1, self._SHADED, 0, 0, 0]
        send_event(self.root, win, data, self._STATE, X.SubstructureRedirectMask)
        
    def doUnShade(self, win):        
        """send unshade event"""
        data = [0, self._SHADED, 0, 0, 0]
        send_event(self.root, win, data, self._STATE, X.SubstructureRedirectMask)

action = '1'
if len(sys.argv) == 2:
    action = sys.argv[1]

if action not in ['0', '1']:
    print('Param must be 0 or 1')
    sys.exit()
    
action = int(action)

X11Shade().run(action)
