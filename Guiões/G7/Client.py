# Código baseado em https://docs.python.org/3.6/library/asyncio-stream.html#tcp-echo-client-using-streams
import asyncio
import socket
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.serialization import load_pem_public_key, PublicFormat, Encoding

from RSA import generatePrivateKey, savePrivateKeyClient, signingMessageClient, verification

# Geração da chave privada do cliente
clientPrivateKey = certificate.generatePrivateKey()

# Geração da chave pública do cliente
clientPublicKey = clientPrivateKey.public_key()

# IV
iv = b'\x8f\x84\x82\xb0\xfc\x19\xe4!\xd6\xf3"\xce\x87o\xe4}'

conn_port = 8888
max_msg_size = 9999

class Client:

    def __init__(self, sckt=None):
        
        self.sckt = sckt
        self.msg_cnt = 0

    def process(self, msg=b"", sharedKey=b""):
        # Número da mensagem
        self.msg_cnt +=1

        print('Input your message.')
        textInput = input().encode()

        # Derivação da shared key para 32 bytes ou seja 256 bits (mais seguro)
        derivedKey = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'\x8f\x84\x82\xb0\xfc\x19\xe4!\xd6\xf3"\xce\x87o\xe4}',
        info=b'handshake data',
        backend=default_backend()
        ).derive(sharedKey)

        # Encriptar a mensagem para mandar ao servidor.
        cipher = Cipher(algorithms.AES(derivedKey), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        
        encryptMessage = encryptor.update(textInput) + encryptor.finalize()
        
        return encryptMessage if len(encryptMessage)>0 else None


@asyncio.coroutine
def tcp_echo_client(loop=None):
    if loop is None:
        loop = asyncio.get_event_loop()

    reader, writer = yield from asyncio.open_connection('127.0.0.1',
                                                        conn_port, loop=loop)
    addr = writer.get_extra_info('peername')
    client = Client(addr)

    certificate.assinar - cria a chave, assinada e devolivda assinada
    write.write(assinatura)
    # Enviar a chave pública para o servidor.
    publicKeyEnviar = clientPublicKey.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)
    writer.write(publicKeyEnviar)

    # Receber a chave pública do Servidor para a criação da Shared Key.
    certificate.vertificar
    publicKeyBytes = yield from reader.read(max_msg_size) -- é o que recebe do Servidor

    publicKeyServer = load_pem_public_key(publicKeyBytes, backend=default_backend())
    sharedKey = clientPrivateKey.exchange(publicKeyServer)
    #print(sharedKey)
    
    msg = client.process(sharedKey=sharedKey)
    while msg:
        writer.write(msg)
        msg = yield from reader.read(max_msg_size)
        if msg :
            msg = client.process(msg=msg, sharedKey=sharedKey)
        else:
            break
    writer.write(b'\n')
    print('Socket closed!')
    writer.close()

def run_client():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tcp_echo_client())


run_client()