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

    while True:
        # print(choicesDict)
        print('1', choicesDict['1'])
        print('2', choicesDict['2'])
        print('3', choicesDict['3'])
        print('4', choicesDict['4'])
        inp = input("Enter your choice, q to quit: ")
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
                print(f'{block.data} , {block.timestamp} , {block.Hash} , {block.prevHash}')
        elif inp=='4':
            print(f'Public Key is: {pubKey}')
        elif inp=='q':
            break
    exit(0)

