#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep

def scroll_text(scroll_text):
    line_length = 80
    scroll_text += " " * ((line_length - 1) - len(scroll_text))

    while True:
        scroll_text = list(scroll_text)

        scroll_text.append(scroll_text.pop(0))

        print("".join(scroll_text), end="\r")

        sleep(0.2)

scroll_text("This is a fancy scrollband!")
