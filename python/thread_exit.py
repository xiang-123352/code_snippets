#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import thread

exit_stat = 0

def child():
    global exit_stat
    
    exit_stat += 1
    
    thread_id = thread.get_ident()
    
    print("Child #: %s %s" % (thread_id, exit_stat))
    
    thread.exit()

def parent():
    while True:
        thread.start_new_thread(child, ())
        
        if raw_input() == "q":
            break

parent()
