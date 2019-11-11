# Código baseado em https://docs.python.org/3.6/library/asyncio-stream.html#tcp-echo-client-using-streams

import asyncio
import socket
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.serialization import load_pem_public_key, PublicFormat, Encoding

# Número primo e valor de gerador dado pelo guião
P = 99494096650139337106186933977618513974146274831566768179581759037259788798151499814653951492724365471316253651463342255785311748602922458795201382445323499931625451272600173180136123245441204133515800495917242011863558721723303661523372572477211620144038809673692512025566673746993593384600667047373692203583
G = 44157404837960328768872680677686802650999163226766694797650810379076416463147265401084491113667624054557335394761604876882446924929840681990106974314935015501571333024773172440352475358750668213444607353872754650805031912866692119819377041901642732455911509867728218394542745330014071040326856846990119719675

# A criação do DH com os números fornecidos no guião
parameters = dh.DHParameterNumbers(P, G, None).parameters(backend=default_backend())

# Geração da chave privada do cliente
clientPrivateKey = parameters.generate_private_key()

# Geração da chave pública do cliente
clientPublicKey = clientPrivateKey.public_key()

# Buscar o mesmo nonce
file = open('nonce.key', 'rb')
nonce = file.read()
file.close()

conn_port = 8888
max_msg_size = 9999
class Client:

    def __init__(self, sckt=None):
        
        self.sckt = sckt
        self.msg_cnt = 0

    def process(self, msg=b"", sharedKey=b""):

        # Number of Message.
        self.msg_cnt +=1

        print('Input your message.')
        textInput = input().encode()

        # Derivação da shared key com 32 bytes ou seja 256 bits (mais seguro)
        derivedKey = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data',
        backend=default_backend()
        ).derive(sharedKey)

        # Encrypt Message to send to Server.
        aesgcm = AESGCM(derivedKey)
        encryptMessage = aesgcm.encrypt(nonce, textInput, None)
        
        return encryptMessage if len(encryptMessage)>0 else None


@asyncio.coroutine
def tcp_echo_client(loop=None):
    if loop is None:
        loop = asyncio.get_event_loop()

    reader, writer = yield from asyncio.open_connection('127.0.0.1',
                                                        conn_port, loop=loop)
    addr = writer.get_extra_info('peername')
    client = Client(addr)

    # Enviar a chave pública para o cliente que entrou.
    publicKeyEnviar = clientPublicKey.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)
    writer.write(publicKeyEnviar)

    # Receber a chave pública do Servidor para a criação da Shared Key.
    publicKeyBytes = yield from reader.read(max_msg_size)
    publicKeyServer = load_pem_public_key(publicKeyBytes, backend=default_backend())
    sharedKey = clientPrivateKey.exchange(publicKeyServer)
    
    msg = client.process()
    while msg:
        writer.write(msg)
        msg = yield from reader.read(max_msg_size)
        if msg :
            msg = client.process(msg, sharedKey)
        else:
            break
    writer.write(b'\n')
    print('Socket closed!')
    writer.close()

def run_client():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tcp_echo_client())


run_client()