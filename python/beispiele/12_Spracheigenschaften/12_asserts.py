# -*- coding: utf-8 -*-

"""
Mittels Asserts lassen sich knappe Konsistenzabfrage erstellen
Bei Gelingen immer True, sonst False -> AssertionError-Exception
"""

import math

#   __debug__ True -> Asserts on
#   __debug__ False -> Asserts off
#   nur über die Kommandozeilenoption -O

#   assert math.sqrt(4) == 1
#   AssertionError
assert math.sqrt(9) == 3
