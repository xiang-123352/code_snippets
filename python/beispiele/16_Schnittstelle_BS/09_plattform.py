# -*- coding: utf-8 -*-

"""
Stellt Informationen zur Hardware und BS zusammen.
Teilweise identisch mit sys
"""

import platform as p

# machine() -> Prozessorarchitektur
print(p.machine())

# node() -> Nerwerkname als String
print(p.node())

# processor() -> Typ und Hersteller CPU
print(p.processor())

# system() -> Name des BS als String
print(p.system())