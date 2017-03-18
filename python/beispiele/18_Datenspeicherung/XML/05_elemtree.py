# -*- coding: utf-8 -*-

import xml.etree.ElementTree as xee

et = xee.parse("test.xml")
e = et.getroot()

print(e.find("*"))
# <Element 'B' at 0x013CF9F0>

print(e.find("E"))
# None

print(e.find("C/*/F"))
# <Element 'F' at 0x013CFB10>

