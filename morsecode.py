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

def morsecode_zu_buchstabe(morsecode):
    for zeichengruppe in morsecode.split(" "):
        for buchstabe in morse_alphabet.keys():
            if zeichengruppe == morse_alphabet[buchstabe]:
                print(buchstabe, end="")

    print()

def foo():
    while True:
        eingabe = input("Morsecode: ")

        if eingabe == "x":
            break
        else:
            morsecode_zu_buchstabe(eingabe)

# Ich will das er mir ganze Sätze in Morsecode übersetzt und umgekeht
#
# Format:
#
# Hallo .-- . .-.. -
# .... .- .-.. .-.. --- welt
#
# Soll es auch piepsen?
#
wort_zu_morsecode("yeah")
wort_zu_morsecode("ascii")
wort_zu_morsecode("art")

#foo()
