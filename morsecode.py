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
    "z":"--..",
    "'":".----.",
    ",":"--..--",
    ".":".-.-.-"
    }

def wort_zu_morsecode(wort):
    wort = wort.lower()
    morsecode_buchstabe = ""

    # morsecode buchstaben getrennt durch ein leerzeichen
    for buchstabe in wort:
        morsecode_buchstabe += morse_alphabet[buchstabe] + " "

    return morsecode_buchstabe.rstrip(" ")

def satz_zu_morsecode(satz):
    morsecode_wort = ""

    # morsecode worte getrennt durch zwei leerzeichen
    for wort in satz.split():
        morsecode_wort += wort_zu_morsecode(wort) + "  "

    return morsecode_wort.rstrip("  ")

def morsecode_zu_wort(morsecode_wort):
    wort = ""

    for morsecode_buchstabe in morsecode_wort.split(" "):
        for buchstabe in morse_alphabet.keys():
            if morsecode_buchstabe == morse_alphabet[buchstabe]:
                wort += buchstabe

    return wort

def morsecode_zu_satz(morsecode_satz):
    morsecode_satz = morsecode_satz.replace("  ", "|")
    satz = ""

    for morsecode_wort in morsecode_satz.split("|"):
        satz += morsecode_zu_wort(morsecode_wort) + " "

    return satz.rstrip(" ")

# Ich will das er mir ganze Sätze in Morsecode übersetzt und umgekeht
#
# Format:
#
# Hallo .-- . .-.. -
# .... .- .-.. .-.. --- welt
#
# Soll es auch piepsen?

if __name__ == '__main__':
    while True:
        eingabe = input("Morsecode: ")

        if eingabe == "x":
            break
        else:
            satz = morsecode_zu_satz(eingabe)

            print(satz)
