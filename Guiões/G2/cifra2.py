import os
import getpass
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
backend = default_backend()

salt = os.urandom(16)

# derivar a chave
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=backend
)

try:
    password = getpass.getpass().encode()
except Exception as error:
    print("Erro na password", error)

key = kdf.derive(password)

# abrir o ficheiro a cifrar
textofile = open('texto.txt', 'rb')
texto = textofile.read()
textofile.close()

# cifrar
f = Fernet(key)
cifra = f.encrypt(texto)

# criar ficheiro com o texto cifrado
fileencrypt = open('cifrado.txt', 'wb')
fileencrypt.write(cifra)
fileencrypt.close()

kdf = PBKDF2HMAC(
     algorithm=hashes.SHA256(),
     length=32,
     salt=salt,
     iterations=100000,
     backend=backend
)

kdf.verify(password, key)