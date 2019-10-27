
class Cifra:

    def enc(self, texto):
    
        cifraCeaser = ''
        for char in texto: 
            if char == ' ':
                cifraCeaser = cifraCeaser + char
            elif  char.isupper():
                cifraCeaser = cifraCeaser + chr((ord(char) + 12 - 65) % 26 + 65)
            else:
                cifraCeaser = cifraCeaser + chr((ord(char) + 12 - 97) % 26 + 97)
        
        return cifraCeaser