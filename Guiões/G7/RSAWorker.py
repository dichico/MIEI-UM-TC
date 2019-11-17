from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key, Encoding, PrivateFormat, NoEncryption
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature

class RSAWorker(object):

    def __init__(self, flag):

        self.rsaPrivateKey = rsa.generate_private_key(
            public_exponent=65537,    
            key_size=2048,    
            backend=default_backend()
        )
        self.rsaPublicKey = self.rsaPrivateKey.public_key()
        self.flag = flag


    # Salvar a Chave Privada do Servidor ou Cliente fazendo já a Serialization.
    def saveRSAPrivateKey(self):
        
        rsaPrivateKey = self.rsaPrivateKey.private_bytes(
            encoding=Encoding.PEM,
            format=PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=NoEncryption()
        )

        if(self.flag==0): nomeFicheiro = "serverPK"
        else: nomeFicheiro = "clientPK"

        with open(nomeFicheiro, "wb") as privateKeyFile:
            privateKeyFile.write(rsaPrivateKey)

    

    # Ler Chave Privada do Servidor ou Cliente.
    def loadPrivateKey(self, flag):

        if(flag==0): nomeFicheiro = "serverPK"
        else: nomeFicheiro = "clientPK"

        with open(nomeFicheiro, "rb") as privateKeyFile:

            self.privateKey = load_pem_private_key(
                privateKeyFile.read(),
                password=None,
                backend=default_backend()
            )

    # Signing - Assinar a mensagem.
    def signingMessage(self, message):

        signature = self.rsaPrivateKey.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature

# Verification.
def verification(self, rsaPublicKey, signature, message):
    try:
        rsaPublicKey.verify(
        signature,
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False
