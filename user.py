from Utils import Users
from RSA import RSA
import getpass
import socket
import pickle, struct

pubKey = (98581262173360837326167111125113695068362686677036762762847714161386363356381, 5)

username = input("Enter Username: ")
password = getpass.getpass(prompt="Enter Password: ")
rsa = RSA()
password = rsa.RSA(password, pubKey[0], pubKey[1])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 6000))
print('Client has been assigned socket name ', sock.getsockname())
creds = '{} {}'.format(username, password)
# sock.sendall(struct.pack("L", len(data))+data)
sock.sendall(creds.encode())
reply = sock.recv(4096)
sock.close()