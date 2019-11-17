from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

# Gerar a Chave Privada tanto para o Cliente como para o Servidor.
def generatePrivateKey() :
    
    privateKey = rsa.generate_private_key(
        public_exponent=65537,    
        key_size=2048,    
        backend=default_backend()
    )

    return privateKey

# Salvar a Chave Privada do Servidor fazendo já o Serialization.
def savePrivateKeyServer(privateKey):
    
    privateKey = privateKey.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    nomeFicheiro = "serverPK"
    with open(nomeFicheiro, "wb") as privateKeyFile:
        privateKeyFile.write(privateKey)
    
    return privateKeyFile

# Salvar a Chave Privada de cada Cliente, consoante o seu número, fazendo já o Serialization.
# O servidor terá de enviar ao Cliente o seu número de Cliente.
def savePrivateKeyClient(privateKey, numeroCliente):
    
    privateKeyEncriptada = privateKey.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    nomeFicheiro = "clientePK" + str(numeroCliente)
    with open(nomeFicheiro, "wb") as privateKeyFile:
        privateKeyFile.write(privateKeyEncriptada)

    return privateKeyFile

# Signing - Assinar a mensagem.
def signingMessageClient(privateKey, message):

    assinatura = privateKey.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

# Verification.
def verification(publicKey, signature, message):

    public_key.verify(
        signature,
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
)

