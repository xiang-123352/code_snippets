"""
file: link_inhalt.py
Functions to capture the links and their content on 
a webpage.
author: brian
"""
import urllib.request
import re

def getHtmlContent(url):
    """Function to convert html bit code to string."""
    try:
        fraw = urllib.request.urlopen(url)
    except HTTPError:
        print ("invalid url")
        return 0

    return fraw.read().decode("utf-8")

def getLinks(htmlText):
    """Function to extract all links on a html-txt file
    and store it in a dictonary."""
    regex = r'<a.*href="(.*)"(?:.*)>(.*)<\/a>'
    result = {}
    tmp = re.findall(regex, htmlText)
    for entry in tmp:
        result[entry[0]] = entry[1]
    return result

print(getHtmlContent("http://www.spiegel.de//"))
test = getLinks(getHtmlContent("https://twython.readthedocs.io/en/latest/"))
test2 = getLinks(getHtmlContent("http://www.spiegel.de//"))




