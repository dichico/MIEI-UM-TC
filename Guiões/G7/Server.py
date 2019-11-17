# Código baseado em https://docs.python.org/3.6/library/asyncio-stream.html#tcp-echo-client-using-streams
import asyncio
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.serialization import load_pem_public_key, PublicFormat, Encoding

# Chave privada do servidor
serverPrivateKey = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# Chave pública do servidor
serverPublicKey = serverPrivateKey.public_key()

# IV
iv = b'\x8f\x84\x82\xb0\xfc\x19\xe4!\xd6\xf3"\xce\x87o\xe4}'

conn_cnt = 0
conn_port = 8888
max_msg_size = 9999

class ServerWorker(object):

    def __init__(self, cnt, addr=None):

        self.idClient = cnt
        self.addr = addr
        self.messageCounter = 0

    def process(self, msg, sharedKey):
        # Número da mensagem.
        self.messageCounter += 1

        # Derivação da shared key para 32 bytes ou seja 256 bits (mais seguro)
        derivedKey = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'\x8f\x84\x82\xb0\xfc\x19\xe4!\xd6\xf3"\xce\x87o\xe4}',
        info=b'handshake data',
        backend=default_backend()
        ).derive(sharedKey)

        # Desencriptar a mensagem vinda do cliente.
        cipher = Cipher(algorithms.AES(derivedKey), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decryptMessage = decryptor.update(msg) + decryptor.finalize()
        
        print('%d' % self.idClient + ": " + decryptMessage.decode())

        return decryptMessage if len(decryptMessage)>0 else None

@asyncio.coroutine
def handle_echo(reader, writer):
    global conn_cnt
    conn_cnt +=1
    addr = writer.get_extra_info('peername')
    srvwrk = ServerWorker(conn_cnt, addr)
    
    # Guardar a chave privada encriptada num ficheiro.
    serverPrivateKeyEncrypted = serverPrivateKey.private_bytes(
        encoding = serialization.Encoding.PEM,
        format = serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm = serialization.NoEncryption()
    )

    filePrivateKey = open('privateKey.key', 'wb')
    fileCrypt.write(serverPrivateKeyEncrypted)
    fileCrypt.close()

    # Receber a chave pública do Cliente para a criação da Shared Key.
    publicKeyBytes = yield from reader.read(max_msg_size)
    publicKeyServer = load_pem_public_key(publicKeyBytes, backend=default_backend())
    sharedKey = serverPrivateKey.exchange(publicKeyServer)

    data = yield from reader.read(max_msg_size)
    while True:
        if not data: continue
        if data[:1]==b'\n': break
        data = srvwrk.process(data, sharedKey)
        if not data: break
        writer.write(data)
        yield from writer.drain()
        data = yield from reader.read(max_msg_size)
    print("[%d]" % srvwrk.idClient + "left.")
    writer.close()


def run_server():
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handle_echo, '127.0.0.1', conn_port, loop=loop)
    server = loop.run_until_complete(coro)
    # Serve requests until Ctrl+C is pressed
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    print('  (type ^C to finish)\n')
    
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
    print('\n Server stopped!')

run_server()