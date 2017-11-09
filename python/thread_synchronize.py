#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import thread
import time

def counter(my_id, count):
    for i in range(count):
        mutex.acquire()
        
        print("[%s] => %s" % (my_id, i))
        
        mutex.release()

mutex = thread.allocate_lock()

for i in range(10):
    thread.start_new_thread(counter, (i, 100))

time.sleep(10)

print("Main thread exiting...")
