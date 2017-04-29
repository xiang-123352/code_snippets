#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import string

tr = str.maketrans("", "", string.punctuation)
s = "Hello! It is time to remove punctuations. It is easy, you will see."

s.translate(tr)

print(s)
