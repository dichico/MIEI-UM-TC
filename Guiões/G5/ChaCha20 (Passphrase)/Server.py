# Código baseado em https://docs.python.org/3.6/library/asyncio-stream.html#tcp-echo-client-using-streams

import asyncio
import random
import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

conn_cnt = 0
conn_port = 8888
max_msg_size = 9999

# Random Key with 256 bits to work on ChaCha20.
key = os.urandom(32)

# Nonce - Not need to be kept secret.
nonce = os.urandom(16)

class ServerWorker(object):

    def __init__(self, cnt, addr=None):

        self.idClient = cnt
        self.addr = addr
        self.messageCounter = 0

    def process(self, msg):

        # Number of Message from Client.
        self.messageCounter += 1

        file = open('key' +self.idClient + '.key', 'rb')
        key = file.read()
        file.close()

        # Divisão dos 64 bits de chave derivada para a chave de encriptação e para a chave para o MAC.
        chaveC = key[:32]
        chaveMAC = key[32:]

        # Algoritmo Chacha20 para a cifragem.
        algorithm = algorithms.ChaCha20(chaveC, nonce)
        cipher = Cipher(algorithm, mode=None, backend = default_backend())
        
        decryptor = cipher.decryptor()
        decryptMessage = decryptor.update(msg[32:])

        print('%d' % self.idClient + ": " + decryptMessage.decode())

        return decryptMessage if len(decryptMessage)>0 else None

@asyncio.coroutine
def handle_echo(reader, writer):
    global conn_cnt
    conn_cnt +=1
    addr = writer.get_extra_info('peername')
    srvwrk = ServerWorker(conn_cnt, addr)
    data = yield from reader.read(max_msg_size)
    while True:
        if not data: continue
        if data[:1]==b'\n': break
        data = srvwrk.process(data)
        if not data: break
        writer.write(data)
        yield from writer.drain()
        data = yield from reader.read(max_msg_size)
    print("[%d]" % srvwrk.idClient)
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
    print('\nFINISHED!')

run_server()