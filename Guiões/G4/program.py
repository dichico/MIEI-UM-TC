import random

from cifra import Cifra 

cifra = Cifra()
key = cifra.keygen()

b =  random.randint(0, 1)

print(key)
print(b)