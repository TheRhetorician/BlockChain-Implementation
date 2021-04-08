import datetime
import pickle
import struct
import hashlib
import json
import socket
from threading import Thread
import os

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
        self.timestamp = datetime.datetime.now().isoformat()
        self.username = username
        self.password = hashlib.sha256(password.encode()).hexdigest()

    def createBlock(self, data):
        return Block(json.dumps(data))

    def mineBlock(self):
        return

    def verifyTransaction(self, currentBlock):
        print("in verify")
        f = open("BlockChain.txt", 'rb')
        blocks = pickle.load(f)
        if currentBlock.prevHash == blocks[-1].Hash:
            f.close()
            return True
        # print(blocks[-1].timestamp, blocks[-1].data, blocks[-1].Hash, blocks[-1].prevHash)
        f.close()
        return False

    def verifyBlockChain(self):
        f = open("BlockChain.txt", 'rb')
        blocks = pickle.load(f)
        for i in range(1,len(blocks)):
            if blocks[i].prevHash != blocks[i-1].Hash:
                return False
        return True

class Admin:
    def __init__(self):
        print("Admin Initiated")
        sock = self.create_socket(('localhost', 5000))
        Thread(target=self.start_threads, args=(sock,)).start()
        if os.stat("BlockChain.txt").st_size == 0:
            f = open('BlockChain.txt', 'wb')
            block = Block("Genesis", '0')
            pickle.dump([block], f)
            f.close()
        if os.stat("Users.txt").st_size == 0:
            f = open('Users.txt', 'wb')
            user = self.createUser('Genesis', 'admin')
            pickle.dump([user], f)
            f.close()


    def createUser(self, username, password):
        print("Inside createUser")
        user = Users(username, password)
        print(user.username, user.password)
        if not os.stat("Users.txt").st_size == 0:
            f = open('Users.txt', 'rb')
            users = pickle.load(f)
            f.close()
            users.append(user)
            f = open('Users.txt', 'wb')
            pickle.dump(users, f)
            f.close()
        return user

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
            self.handle_conversation(sock,address)

    def handle_conversation(self, sock, address):
        try:
            while True:
                sock.sendall('Start Proof of work')
                self.handle_request(sock)
        except EOFError:
            print('Client socket to {} has closed'.format(address))
        except Exception as e:
            print('Client {} error {}'.format(address,e))
        finally:
            sock.close()

    def handle_request(self, sock):
        data = b''
        payload_size = struct.calcsize("L")
        print("Expecting Data")
        while len(data) < payload_size:
            data += sock.recv(4096)
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("L", packed_msg_size)[0]
        while len(data) < msg_size:
            data += sock.recv(4096)
        block_data = data[:msg_size]
        data = data[msg_size:]
        block = pickle.loads(block_data)

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
        print("here")
        t = (listener,)
        for i in range(workers):
            Thread(target=self.accept_forever, args=t).start()
        return

    

        

val = {"Name":'Hardik', "Age":22}
result = json.dumps(val)
# print(result)
# bl = Block(result)
ad = Admin()
print("After initialisation")
# ad.createUser("Hardik", "Hello")
# print("After create User")
f = open("Users.txt", "rb")
users = pickle.load(f)
# for i in range(0,len(users)):
#     print(users[i].timestamp, users[i].username, users[i].password)
f.close()
f = open('BlockChain.txt', 'rb')
blocks = pickle.load(f)
for i in range(0,len(blocks)):
    print(blocks[i].data, blocks[i].timestamp, blocks[i].Hash, blocks[i].prevHash)
f.close()
prevHash = blocks[-1].Hash
block = Block(result, prevHash)
# f = open('BlockChain.txt', 'wb')
# blocks.append(block)
# pickle.dump(blocks, f)
# f.close()
print(users[1].verifyBlockChain())