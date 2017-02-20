#!/usr/bin/env python3
# -*- coding: utf-8 -*-

lower_case = "abcdefghijklmnopqrstuvwxyz"
upper_case = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
umlauts = "äöüßÄÖÜ"
numbers = "1234567890"
signs = ".:,;?!() "
alnum = lower_case + upper_case + umlauts + numbers

sentence = "1, 2, 3, 4, 5, 6, 7, meine Mutter, die kocht Rüben."
word = ""
word_list = []

for letter in sentence:
    if letter in alnum:
        word += letter
    else:
        if len(word) > 0: # filter empty words from the word list
            word_list.append(word)

            word = ""

print(word_list)
