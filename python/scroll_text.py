#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep

def scroll_text(str, reverse=False):
    for i, _ in enumerate(str):
        if reverse:
            i = -i

        print("%s%s" % (str[i:], str[:i]), end="\r")

        sleep(0.2)

    print("%s" % str, end="\r")

while True:
    scroll_text("This is a fancy scrollband!")
