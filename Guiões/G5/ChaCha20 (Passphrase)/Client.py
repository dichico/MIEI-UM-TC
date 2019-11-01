# Código baseado em https://docs.python.org/3.6/library/asyncio-stream.html#tcp-echo-client-using-streams

import asyncio
import socket
import getpass

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.fernet import Fernet

conn_port = 8888
max_msg_size = 9999

class Client:

    def __init__(self, sckt=None):
        
        self.sckt = sckt
        self.msg_cnt = 0

    def process(self, msg=b""):

        # Number of Message.
        self.msg_cnt +=1
        
        # Obter randoms para o Salt e Nonce.
        salt = os.urandom(16)
        nonce = os.urandom(16)

        # Criar instância da classe PBKDF2HMAC.
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=64,
            salt=salt,
            iterations=100000,
            backend = default_backend()
        )
        
        # Perguntar/Guardar a passphrase dada pelo User.
        try:
            password = getpass.getpass().encode()
        except Exception as error:
            print("Erro na password", error)

        # Derivação da passphrase.
        key = kdf.derive(password)


        # Saved to a file.
        file = open('key' +self.msg_cnt + '.key', 'wb')
        file.write(key)
        file.close()

        # Divisão dos 64 bits de chave derivada para a chave de encriptação e para a chave para o MAC.
        chaveC = key[:32]
        chaveMAC = key[32:]

        textInput = input().encode()

        # Algoritmo Chacha20 para a cifragem.
        algorithm = algorithms.ChaCha20(chaveC, nonce)
        cipher = Cipher(algorithm, mode=None, backend = default_backend())
        
        encryptor = cipher.encryptor()
        mensagemEncriptada = encryptor.update(textInput)

        # Parte HMAC já com o criptograma.
        mac = hmac.HMAC(chaveMAC, hashes.SHA256(), backend = default_backend())
        mac.update(mensagemEncriptada)
        tagMAC = mac.finalize()

        encryptMessage = tagMAC + mensagemEncriptada
        
        return encryptMessage if len(encryptMessage)>0 else None


@asyncio.coroutine
def tcp_echo_client(loop=None):
    if loop is None:
        loop = asyncio.get_event_loop()

    reader, writer = yield from asyncio.open_connection('127.0.0.1',
                                                        conn_port, loop=loop)
    addr = writer.get_extra_info('peername')
    client = Client(addr)
    msg = client.process()
    while msg:
        writer.write(msg)
        msg = yield from reader.read(max_msg_size)
        if msg :
            msg = client.process(msg)
        else:
            break
    writer.write(b'\n')
    print('Socket closed!')
    writer.close()

def run_client():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tcp_echo_client())


run_client()