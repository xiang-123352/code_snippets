#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import re
import subprocess

def download_page(url):
    html_file = url.split("/")[-1]

    subprocess.check_output(["wget", "-q", "-O", html_file, url])
    
    return html_file

def html2text(html_file):
    if html_file.endswith(".html"):
        text_file = html_file.rsplit(".html")[0] + ".txt"
    elif html_file.endswith(".htm"):
        text_file = html_file.rsplit(".htm")[0] + ".txt"
    else:
        text_file = html_file + ".txt"
    
    subprocess.check_output(["html2text", "-o", text_file, "-utf8", html_file])

    return text_file

def show_result(regex, text):
    match_iter = re.findall(regex, text)

    for match in match_iter:
        print(match)

url = "https://de.wikipedia.org/wiki/Rufnummer"
html_file = download_page(url)
text_file = html2text(html_file)
text = open(text_file).read()
regex = ""

while regex != ":q":
    regex = raw_input("RegEx: ")
    
    show_result(regex, text)
