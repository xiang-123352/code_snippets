#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import re
import subprocess

def show_result(regex, text):
    match_iter = re.finditer(regex, text)

    for match in match_iter:
        print(match.group())

url = "https://de.wikipedia.org/wiki/Rufnummer"
text = subprocess.check_output(["links", "-dump", url])
regex = ""

while regex != ":q":
    regex = raw_input("RegEx: ")
    
    show_result(regex, text)
