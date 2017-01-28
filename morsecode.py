#!/usr/bin/env python3

morse_alphabet = {
    "a":".-",
    "b":"-...",
    "c":"-.-.",
    "d":"-..",
    "e":".",
    "f":"..-.",
    "g":"--.",
    "h":"....",
    "i":"..",
    "j":".---",
    "k":"-.-",
    "l":".-..",
    "m":"--",
    "n":"-.",
    "o":"---",
    "p":".--.",
    "q":"--.-",
    "r":".-.",
    "s":"...",
    "t":"-",
    "u":"..-",
    "v":"...-",
    "w":".--",
    "x":"-..-",
    "y":"-.--",
    "z":"--.."
    }

def wort_zu_morsecode(wort):
    wort = wort.lower()

    for buchstabe in wort:
        print(morse_alphabet[buchstabe], end=" ")

    print()

def morsecode_zu_wort(morsecode):
    for wort in morsecode.split(" "):
        print(wort)

# Ich will das er mir ganze Sätze in Morsecode übersetzt und umgekeht
# Format:
# Hallo .-- . .-.. -
# .... .- .-.. .-.. --- welt

wort_zu_morsecode("hallo")
wort_zu_morsecode("welt")

morsecode_zu_wort(".... .- .-.. .-.. ---")
