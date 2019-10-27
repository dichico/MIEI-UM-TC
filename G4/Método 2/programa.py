import random
import string

from cifraCeaser import Cifra 
from adversario import Adversario

cifra = Cifra()
adversario = Adversario()

m = ["NULL", "NULL"]

enc_oracle = lambda texto: cifra.enc(texto)

# Damos ao atacante dois textos que depois serão encriptados.
m[0], m[1] = adversario.choose()

b =  random.randint(0, 1)
c = cifra.enc(m[b])

bLinha = adversario.guess(enc_oracle, c)

print("Mensagem 0 Cifrada: " + m[0])
print("Mensagem 1 Cifrada: " + m[1])
print()
print("Mensagem Escolhida " + str(b))
print("Mensagem Escolhida cifrada " + c)
print()
print("Adivinhou Mensagem?")
print(b==bLinha)