import random

from cifra import Cifra 
from adversario import Adversario

cifra = Cifra()
adversario = Adversario("OLAAA", "TUDO")

m = [0, 1]

textofile = open('texto.txt', 'rb')
texto = textofile.read()
textofile.close()

key = cifra.keygen()
enc_oracle = lambda ptxt: cifra.enc(key, ptxt)
m[0], m[1] = adversario.choose(enc_oracle(texto))
b =  random.randint(0, 1)
c = cifra.enc(key, m[b])
bLinha = adversario.guess(enc_oracle(texto), c)

print(c)
print(bLinha)

print(b==bLinha)