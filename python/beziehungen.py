class Herz:
    def __init__(self):
        #self.mensch = Mensch() # Abhängig - Komposition
        print("Boom, Boom, Boom ....")


class Adresse:
    def __init__(self):
        print("Ich bin eine Adresse")
        self.str = "Musterstraße"
        self.hnr = 20
        self.ort = "Musterhausen"
        self.plz = 12345

    def __str__(self):
        return self.str + ", " + str(self.hnr) + ", " + self.ort + ", " + str(self.plz)



class Mensch:
    def __init__(self):
        self.herz = Herz() # Abhängig - Komposition
        print("Huhu, da bin ich")
        self.addr = ""

    def set_addr(self, addr):
        self.addr = addr

    def get_addr(self):
        return self.addr


m = Mensch()
a = Adresse()
m.set_addr(a) # Unabhängig - Aggregation
print(m.get_addr())