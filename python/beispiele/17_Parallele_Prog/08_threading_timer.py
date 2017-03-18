# -*- coding: utf-8 -*-


"""
Entspricht einem Delay
"""

import time, threading

def wecker(gestellt):
    print("RIIIIIIIIIING!!!")
    print("Der Wecker wurde um {0} Uhr gestellt.".format(gestellt))
    print("Es ist {0} Uhr".format(time.strftime("%H:%M:%S")))

timer = threading.Timer(30, wecker, [time.strftime("%H:%M:%S")])

# Timer start -> T minus 30 Sekunden
# bis RIIIIIIIIIIING
timer.start()