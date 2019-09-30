from cryptography.fernet import Fernet

key = Fernet.generate_key()

# só a guardar a chave
file = open('chave.key', 'wb')
file.write(key)
file.close()

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
# ------
# buscar chave
file = open('chave.key', 'rb')
chave = file.read()
file.close()

# buscar texto cifrado
filecifrado = open('cifrado.txt', 'rb')
textocifrado = filecifrado.read()
filecifrado.close()

# decrypt com a chave do ficheiro
f2 = Fernet(chave)
final = f2.decrypt(textocifrado)
print(final)