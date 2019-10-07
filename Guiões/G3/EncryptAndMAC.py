import os
import getpass
import base64

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac

# Obter as chaves Crypt e MAC
salt = os.urandom(16)
nonce = os.urandom(16)

kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=64,
    salt=salt,
    iterations=100000,
    backend = default_backend()
)

try:
    password = getpass.getpass().encode()
except Exception as error:
    print("Erro na password", error)

key = kdf.derive(password)

# FASE 1 - Encriptar

# Parte Encrypt

algorithm = algorithms.ChaCha20(chaveC, nonce)

# Abrir o ficheiro a crifrar
textofile = open('texto.txt', 'rb')
textoCrifar = textofile.read()
textofile.close()

#Cifrar
cipher = Cipher(algorithm, mode=None, backend = default_backend())
encryptor = cipher.encryptor()
mensagemEncriptada = encryptor.update(textoCrifar)

# Parte HMAC

mac = hmac.HMAC(chaveMAC, hashes.SHA256(), backend = default_backend())
mac.update(textoCrifar)
tagMAC = mac.finalize()

# Guardar o criptograma
fileCrypt = open('textoCrypt.txt', 'wb')
fileCrypt.write(mensagemEncriptada)
fileCrypt.close()

# Guardar a tag MAC
fileMAC = open('tagMAC.txt', 'wb')
fileMAC.write(tagMAC)
fileMAC.close()

# FASE 2 - Desencriptar

decryptor  = cipher.decryptor()
print(decryptor.update(mensagemEncriptada))
