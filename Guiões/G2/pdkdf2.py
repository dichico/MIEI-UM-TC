import os
import getpass
import base64

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

backend = default_backend()
salt = os.urandom(16)

# criar o kdf
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

# só a guardar a chave derivada
file = open('chave.key', 'wb')
file.write(key)
file.close()

# abrir o ficheiro a cifrar
textofile = open('texto.txt', 'rb')
texto = textofile.read()
textofile.close()

# cifrar
key = base64.urlsafe_b64encode(key)
f = Fernet(key)
cifra = f.encrypt(texto)

# criar ficheiro com o texto cifrado
fileencrypt = open('cifrado.txt', 'wb')
fileencrypt.write(cifra)
fileencrypt.close()

# ------
# buscar chave
file = open('chave.key', 'rb')
chave = file.read()
file.close()

kdf2 = PBKDF2HMAC(
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

kdf2.verify(password, chave)

# buscar texto cifrado
filecifrado = open('cifrado.txt', 'rb')
textocifrado = filecifrado.read()
filecifrado.close()

# decrypt com a chave do ficheiro
chave = base64.urlsafe_b64encode(chave)
f2 = Fernet(chave)
final = f2.decrypt(textocifrado)
print(final)