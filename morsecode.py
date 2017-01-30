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
    morsecode = ""

    # buchstaben getrennt durch ein leerzeichen
    for buchstabe in wort:
        morsecode += morse_alphabet[buchstabe] + " "

    return morsecode.rstrip(" ")

def satz_zu_morsecode(satz):
    morsecode = ""

    # worte getrennt durch zwei leerzeichen
    for wort in satz.split():
        morsecode += wort_zu_morsecode(wort) + "  "

    return morsecode.rstrip("  ")

def morsecode_zu_wort(morsecode):
    wort = ""

    for zeichengruppe in morsecode.split(" "):
        for buchstabe in morse_alphabet.keys():
            if zeichengruppe == morse_alphabet[buchstabe]:
                wort += buchstabe

    return wort

def morsecode_zu_satz(morsecode):
    satz_morsecode = morsecode.replace("  ", "|")
    satz = ""

    for wort in satz_morsecode.split("|"):
        satz += morsecode_zu_wort(wort) + " "

    return satz.rstrip(" ")

# Ich will das er mir ganze Sätze in Morsecode übersetzt und umgekeht
#
# Format:
#
# Hallo .-- . .-.. -
# .... .- .-.. .-.. --- welt
#
# Soll es auch piepsen?
#
satz = morsecode_zu_satz("-.-- . .- ....  .- ... -.-. .. ..  .- .-. -")
print(satz)
