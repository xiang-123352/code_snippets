# -*- coding: utf-8 -*-

geheimnis = 1234
versuch = 0
anzahl = 0

while versuch != geheimnis:
    versuch = input("Raten Sie: ")
    if versuch == "ende":
        print("Und Tschüß")
        break
    else:
        if versuch.isdigit():
            versuch = int(versuch)
            anzahl += 1
            if versuch > geheimnis:
                print("zu gross")                
            elif versuch < geheimnis:
                print("zu klein")
            else:
                if anzahl > 1:            
                    print("Glückwunsch. Nur",anzahl,"Versuche gebraucht.")
                else:
                    print("Glückwunsch. Nur",anzahl,"Versuch gebraucht.")
        else:
            print("Geben Sie eine gültige Zahl ein oder 'ende' für Ende")        
