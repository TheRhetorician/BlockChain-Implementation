import datetime
import pickle
import hashlib
import json
import socket
from threading import Thread

class Block:
    def __init__(self, data, prevHash=''):
        self.data = data
        self.timestamp = datetime.datetime.now().isoformat()
        self.prevHash = prevHash
        self.Hash = self.calculateHash()
        # print(self.Hash)

    def calculateHash(self):
        return hashlib.sha256((self.timestamp + self.prevHash + self.data).encode()).hexdigest()

class Users:
    def __init__(self, username, password):
        self.username = username
        self.password = hashlib.sha256(password.encode()).hexdigest()

    def createBlock(self, data):
        return Block(json.dumps(data))

    def mineBlock(self):
        return

    def verifyTransaction(self):
        return None

    def verifyBlockChain(self):
        return

class Admin:
    def __init__(self):
        print("Admin Initiated")
        self.sock = self.create_socket(('localhost', 5000))

    def create_socket(self, address):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind(address)
        listener.listen(64)
        print('listening at {}'.format(address))
        return listener

    def accept_forever(self, listener):
        while True:
            sock, address = listener.accept()
            print('Accepted connection from {}'.format(address))
            handle_conversation(sock,address)

    def handle_conversation(self, sock, address):
        try:
            while True:
                handle_request(sock)
        except EOFError:
            print('Client socket to {} has closed'.format(address))
        except Exception as e:
            print('Client {} error {}'.format(address,e))
        finally:
            sock.close()

    def handle_request(self, sock):
        task = recv_untill(sock,b'?')
        ans = get_ans(task)
        sock.sendall(ans)

    def recv_untill(self, sock, suffix):
        msg = sock.recv(4096)
        if not msg:
            raise EOFError('socket closed')
        while not msg.endswith(suffix):
            data = sock.recv(4096)
            if not data:
                raise IOError('received {!r} then socket closed'.format(msg))
            msg+=data
        return msg

    def get_ans(self, task):
        # time.sleep(2)
        # return tasks.get(task, b'Error: Unknown task')
        return

    def start_threads(self, listener, workers=4):
        t = (listener,)
        for i in range(workers):
            Thread(target=accept_forever, args=t).start()

    

        

# val = {"Name":'Hardik', "Age":22}
# result = json.dumps(val)
# print(result)
# bl = Block(result)