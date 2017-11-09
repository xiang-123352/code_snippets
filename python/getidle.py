#!/usr/bin/python

import time

def getidle(cpu=""):
    f = open("/proc/stat")
    for l in f:
        l = l.split()
        if l[0] == "cpu"+cpu:
            break
    return int(l[4])

def idle(cpu=""):
    idle1 = getidle(cpu)
    time.sleep(1)
    idle2 = getidle(cpu)
    return (idle2-idle1)/100.0

if __name__ == "__main__":
    cpu0_load = idle("0")
    cpu1_load = idle("1")

    print 1.0 - cpu0_load
    print 1.0 - cpu1_load

