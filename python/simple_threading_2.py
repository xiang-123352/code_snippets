#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import urllib2
from threading import Thread

def btl_test():                                                                                                                                 while 1:                                                                            
    page = urllib2.urlopen("example.com")                                                                                                             

for i in range(120):                                                                                                                        
    t = Thread(target=btl_test)                                                                                                           
    t.start()

