# Código baseado em https://docs.python.org/3.6/library/asyncio-stream.html#tcp-echo-client-using-streams

import asyncio
import socket
from cryptography.fernet import Fernet

conn_port = 8888
max_msg_size = 9999

crypt = Fernet('sqcyNL5kz2mxWb1KL2QSZWY-GCERE-scEgWBbvq9CCk=')

class Client:

    def __init__(self, sckt=None):
        
        self.sckt = sckt
        self.msg_cnt = 0

    def process(self, msg=b""):

        # Number of Message
        self.msg_cnt +=1

        print('Input your message.')
        new_msg = input().encode()
        encryptMessage = crypt.encrypt(new_msg)
        
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