from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key, Encoding, PrivateFormat, NoEncryption, PublicFormat
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature

class RSAWorker(object):

    # Inicialização das variáveis, ou seja, as chaves privadas e públicas
    def __init__(self, flag):

        self.rsaPrivateKey = rsa.generate_private_key(
            public_exponent=65537,    
            key_size=2048,    
            backend=default_backend()
        )
        self.rsaPublicKey = self.rsaPrivateKey.public_key()
        self.flag = flag


    # Salvar a Chave Privada do Servidor ou Cliente fazendo já a Serialization.
    def saveRSAKeys(self):
        
        # Criação dos bytes serializados da chave RSA privada.
        privateBytes = self.rsaPrivateKey.private_bytes(
            encoding=Encoding.PEM,
            format=PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=NoEncryption()
        )

        # Criação dos bytes serializados da chave RSA pública.
        publicBytes = self.rsaPublicKey.public_bytes(encoding=Encoding.PEM,
            format=PublicFormat.SubjectPublicKeyInfo)

        # Guardar no ficheiro a chave pública.
        if(self.flag==0): nomeFicheiro = "serverRSA.private"
        else: nomeFicheiro = "clientRSA.private"
        with open(nomeFicheiro, "wb") as privateKeyFile:
            privateKeyFile.write(privateBytes)

        # Guardar no ficheiro a chave pública.
        if(self.flag==0): nomeFicheiro = "serverRSA.public"
        else: nomeFicheiro = "clientRSA.public"
        with open(nomeFicheiro, "wb") as publicKeyFile:
            publicKeyFile.write(publicBytes)


    # Ler Chave Privada do Servidor ou Cliente (é necessário?)
    def loadPrivateKey(self, flag):

        if(flag==0): nomeFicheiro = "serverRSA.private"
        else: nomeFicheiro = "clientRSA.private"

        with open(nomeFicheiro, "rb") as privateKeyFile:

            self.privateKey = load_pem_private_key(
                privateKeyFile.read(),
                password=None,
                backend=default_backend()
            )

    # Assinar a mensagem com a chave privada RSA.
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

# Função standalone para verificar uma assinatura fornecendo também a chave pública RSA.
def verification(rsaPublicKey, signature, message):
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

# Função standalone para efetuar o loading da chave pública RSA.
def loadPublicKey(flag, numCliente=0):
    
    if(flag==0): nomeFicheiro = "serverRSA.public"
    else: nomeFicheiro = "clientRSA" + numCliente + ".public"

    with open(nomeFicheiro, "rb") as publicKeyFile:
        
        publicRSAKey = load_pem_public_key(
            publicKeyFile.read(),
            backend=default_backend()
        )

    return publicRSAKey