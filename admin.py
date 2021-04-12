from Utils import Admin, Block, Users
import socket
import pickle
import struct
import getpass
pubKey = (98581262173360837326167111125113695068362686677036762762847714161386363356381, 5)


if __name__ =='__main__':
    ad = Admin()
    choicesDict = {
        '1':'Create New User',
        '2':'View All Users', 
        '3':'View Current BlockChain',
        '4':'View Admin\'s Public Key'
    }
    print(choicesDict)
    inp = input("Enter your choice, q to quit: ")

    while True:
        if inp=='1':
            username = input("\tEnter Username: ")
            password = getpass.getpass(prompt="\tEnter Password: ")
            ad.createUser(username, password)
        elif inp=='2':
            f = open('Users.txt', 'rb')
            users = pickle.load(f)
            f.close()
            for user in users:
                print(f'Username: {user.username} , Timestamp: {user.timestamp}')
        elif inp=='3':
            f = open('BlockChain.txt', 'rb')
            blocks = pickle.load(f)
            f.close()
            for block in blocks:
                print(f'{block.data} , {block.timestamp}')
        elif inp=='4':
            print(f'Public Key is: {pubKey}')
        elif inp=='q':
            break
        inp = input("Enter your choice, q to quit: ")
    exit(0)

