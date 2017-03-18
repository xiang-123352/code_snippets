"""
Blockkommentar
Das ist mein erstes Game
geschrieben in Python
"""
# Zeilenkommentar
geheimnis = 1234
versuch = 0
zaehler = 0
while versuch != geheimnis:
    versuch = int(input("Raten Sie:"))
    if versuch < geheimnis:
            print("zu klein")
    if versuch > geheimnis:
            print("zu gross")
    # ES GIBT KEINE INKREMENTOREN UND AUCH KEINE DEKREMENTOREN
    #zaehler = zaehler + 1
    zaehler += 1

print("Super. Sie haben es in ",zaehler," Versuchen geschafft")