import datetime
import pickle
import struct
import hashlib
import json
import socket
from threading import Thread
import os, sys
import random

class Block:
    def __init__(self, data, prevHash='', nonce = 0):
        self.data = data
        self.timestamp = datetime.datetime.now().isoformat()
        self.prevHash = prevHash
        self.nonce = nonce
        self.Hash = self.calculateHash()
        print(self.Hash, len(self.Hash))

    def calculateHash(self):
        return hashlib.sha256((self.timestamp + self.prevHash + self.data + str(self.nonce)).encode()).hexdigest()

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

    def verifyPoW(self, block):
        val = hashlib.sha256((block.timestamp + block.prevHash + block.data + str(block.nonce)).encode()).hexdigest()
        if val != block.Hash:
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
        hashbool = 0
        for i in range(0,len(users)):
            # transact = users[i].verifyTransaction(block)
            hashing = users[i].verifyPoW(block)
            # if transact:
            #     transactbool+=1
            if hashing:
                hashbool+=1
        print(transactbool, hashbool)
        if hashbool > len(users)/2: #and transactbool > len(users)/2 and :
            return True
        return False

    def addBlock(self, block):
        f = open('BlockChain.txt', 'rb')
        blocks = pickle.load(f)
        f.close()
        blocks.append(block)
        f = open('BlockChain.txt', 'wb')
        pickle.dump(blocks, f)
        f.close()
        f = open('Users.txt', 'rb')
        users = pickle.load(f)
        f.close()
        for i in range(0,len(users)):
            users[i].blockChain = blocks
        return

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
                print("Mining not verified by consensus of the users")
                return
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
        self.mineBlock(block)
        toProceed = self.checkData(block)
        if not toProceed:
            return False
        print("PoW done by miner verified by consensus of users")
        self.addBlock(block)
        sock.sendall('Block has been added to the BlockChain'.encode())
        return True

    def mineBlock(self, block, difficulty = 4):
        while block.Hash[:difficulty] != '0'*difficulty:
            block.nonce+=1
            block.Hash = block.calculateHash()
        print(block.nonce, block.Hash)
        return

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
# # # print("After initialisation")
# # # ad.createUser("Daksh", "Nobody")
# # # print("After create User")
# # f = open("Users.txt", "rb")
# # users = pickle.load(f)
# # for i in range(0,len(users)):
# #     print(users[i].timestamp, users[i].username, users[i].password, users[i].blockChain)
# #     print(users[i].verifyBlockChain())
# # f.close()
# f = open('BlockChain.txt', 'rb')
# blocks = pickle.load(f)
# for i in range(0,len(blocks)):
#     print(blocks[i].data, blocks[i].timestamp, blocks[i].Hash, blocks[i].prevHash)
# f.close()
# # print(Admin().power(2, 5, 11))

# # print(users[1].verifyBlockChain())

# val = {"Name":'Kriti', "Age":20}
# result = json.dumps(val)
# # print(result)
# # bl = Block(result)
# f = open('BlockChain.txt', 'rb')
# blocks = pickle.load(f)
# f.close()
# prevHash = blocks[-1].Hash
# block = Block(result, prevHash)
# print(block.data, block.timestamp, block.Hash, block.prevHash)
f = open('BlockChain.txt', 'rb')
blocks = pickle.load(f)
f.close()
val = {"Name":'Hardik', "Age":22}
result = json.dumps(val)
# print(result)
bl = Block(result, blocks[-1].Hash)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 5000))
print('Client has been assigned socket name ', sock.getsockname())
# # sock.sendall(b'Hello server, we are using TCP protocol for communication')
reply = sock.recv(4096)
print('The server said\n', repr(reply.decode()))
data = pickle.dumps(bl) 
sock.sendall(struct.pack("L", len(data))+data)
reply = sock.recv(4096)
sock.close()

f = open('BlockChain.txt', 'rb')
blocks = pickle.load(f)
for i in range(0,len(blocks)):
    print(blocks[i].data, blocks[i].timestamp, blocks[i].Hash, blocks[i].prevHash, 'nonce: ', blocks[i].nonce)
f.close()

# ad.mineBlock(bl, 5)