import datetime
import pickle
import struct
import hashlib
import json
import socket
from threading import Thread
import os
import random

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
        self.blockChain = []

    def createBlock(self, data):
        return Block(json.dumps(data))

    def verifyTransaction(self, currentBlock):
        print("in verify")
        f = open("BlockChain.txt", 'rb')
        blocks = pickle.load(f)
        # blocks = self.blockChain
        print(currentBlock.prevHash)
        print(blocks[-1].Hash)
        if currentBlock.prevHash == blocks[-1].Hash:
            print("yes")
            return True
        # print(blocks[-1].timestamp, blocks[-1].data, blocks[-1].Hash, blocks[-1].prevHash)
        f.close()
        return False

    def verifyBlockChain(self):
        # f = open("BlockChain.txt", 'rb')
        # blocks = pickle.load(f)
        blocks = self.blockChain
        for i in range(1,len(blocks)):
            if blocks[i].prevHash != blocks[i-1].Hash:
                return False
        return True

class Admin:                #Miner
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
        if not os.stat("BlockChain.txt").st_size == 0:
            f = open('BlockChain.txt', 'rb')
            blocks = pickle.load(f)
            f.close()
            user.blockChain = blocks
        # print(user.username, user.password)
        if not os.stat("Users.txt").st_size == 0:
            f = open('Users.txt', 'rb')
            users = pickle.load(f)
            f.close()
            users.append(user)
            f = open('Users.txt', 'wb')
            pickle.dump(users, f)
            f.close()
        return user

    def checkData(self, block):
        f = open('Users.txt','rb')
        users = pickle.load(f)
        f.close()
        transactbool = 0
        chainbool = 0
        for i in range(0,len(users)):
            transact = users[i].verifyTransaction(block)
            chain = users[i].verifyBlockChain()
            if transact:
                transactbool+=1
            if chain:
                chainbool+=1
        print(transactbool, chainbool)
        if transactbool > len(users)/2 and chainbool > len(users)/2:
            return True
        return False

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
            val = self.handle_request(sock)
            if not val:
                return
                # break
        except EOFError:
            print('Client socket to {} has closed'.format(address))
        except Exception as e:
            print('Client {} error {}'.format(address,e))
        finally:
            sock.close()

    def handle_request(self, sock):
        data = b''
        payload_size = struct.calcsize("L")
        sock.sendall('Send Block'.encode())
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
        toProceed = self.checkData(block)
        if not toProceed:
            return False
        print("Block verified by Users")
        i = 3
        sock.sendall(('Start Proof of work itertions = {}'.format(i)).encode())
        print("Mining Started")
        while i:
            val = self.mineBlock(sock, i)
            i-=1
            if not val:
                return False
        print("Mining ended")
        return True

    def power(self, x, y, p):
        res = 1 
        x = x % p
        while (y > 0):
            if (y & 1):
                res = (res * x) % p
            y = y >> 1
            x = (x * x) % p
        return res

    def mineBlock(self, sock, i):
        data = sock.recv(4096)
        b = random.randint(0,1)
        sock.sendall(str(b).encode())
        data = data.decode()
        # print(data)
        data = data.split()
        g = int(data[0])
        y = int(data[1])
        h = int(data[2])
        print(g,y,h)
        print('b in mineBlock is ', b)
        data = sock.recv(4096)
        data = data.decode()
        data = data.split()
        # print(data)
        s = int(data[0])
        print('s is ', s)
        p=11
        print("Mining {} started".format(i))
        one = self.power(g,s,p)
        two = ((h%p)*(y**b)%p)%p
        print("Mining {} ended".format(i))
        print(one, two)
        return one == two

    def start_threads(self, listener, workers=4):
        print("here")
        t = (listener,)
        for i in range(workers):
            Thread(target=self.accept_forever, args=t).start()
        return

    

        

# val = {"Name":'Sristi', "Age":21}
# result = json.dumps(val)
# # print(result)
# # bl = Block(result)
# blocks.append(block)
# f = open('BlockChain.txt', 'wb')
# pickle.dump(blocks, f)
# f.close()
ad = Admin()
# # print("After initialisation")
# # ad.createUser("Daksh", "Nobody")
# # print("After create User")
# f = open("Users.txt", "rb")
# users = pickle.load(f)
# for i in range(0,len(users)):
#     print(users[i].timestamp, users[i].username, users[i].password, users[i].blockChain)
#     print(users[i].verifyBlockChain())
# f.close()
f = open('BlockChain.txt', 'rb')
blocks = pickle.load(f)
for i in range(0,len(blocks)):
    print(blocks[i].data, blocks[i].timestamp, blocks[i].Hash, blocks[i].prevHash)
f.close()
# print(Admin().power(2, 5, 11))

# print(users[1].verifyBlockChain())

val = {"Name":'Kriti', "Age":20}
result = json.dumps(val)
# print(result)
# bl = Block(result)
f = open('BlockChain.txt', 'rb')
blocks = pickle.load(f)
f.close()
prevHash = blocks[-1].Hash
block = Block(result, prevHash)
print(block.data, block.timestamp, block.Hash, block.prevHash)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 5000))
print('Client has been assigned socket name ', sock.getsockname())
# sock.sendall(b'Hello server, we are using TCP protocol for communication')
reply = sock.recv(4096)
print('The server said\n', repr(reply.decode()))
data = pickle.dumps(block) ### new code
sock.sendall(struct.pack("L", len(data))+data)
reply = sock.recv(4096)
iterations = reply.decode().split()
iterations = int(iterations[-1])

print('iterations are ',iterations)
while iterations:
    sock.sendall((str(2) + " " + str(10) + " " + str(7)).encode())
    b = sock.recv(4096)
    b = b.decode()
    b = b.split()
    print(b[0])
    b = int(b[0])
    print('b is ',b)
    s = (7+5*b)%10
    sock.sendall((str(s) + " ").encode())
    print(type(b))
    iterations-=1
sock.close()