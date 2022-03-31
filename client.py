import socket
import random
import argparse
import time
import threading


FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DC"

argParser = argparse.ArgumentParser(description='Connect to the chat room. Example: client.py localhost 4242 Steven')
argParser.add_argument('IP', type=str, help='IP address of the server the client is connecting to.')
argParser.add_argument('port', type=int, help='The port the client is connecting to (Integers only).')
argParser.add_argument('name', type=str, help='The name of the client. Connect as a host or a bot(Ash, Misty or Brock)')
args = argParser.parse_args()
IP = args.IP
port = args.port
name = args.name

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, port))


bots = ["ola", "seb", "fred", "haakon"]


good_things = ["laugh", "play", "relax", "read", "train", "sleep"]
bad_things = ["scream", "fight", "moan", "bicker", "complain", "kill"]


def receivemessage():
    while True:
        message = client.recv(2048).decode(FORMAT)
        print(message)


def clientsend(msg):
    # print(msg)
    message = msg.encode(FORMAT)
    client.send(message)


def messages():
    msgs = True
    while msgs:
        clientmsg = input("")
        clientsend(clientmsg)
        if clientmsg == DISCONNECT_MESSAGE:
            print("\nDisconnected from the chat room\n")
            msgs = False

        if msgs == "":
            print("\nPlease type something!")
            continue


message_thread = threading.Thread(target=messages)
message_thread.start()
receive_thread = threading.Thread(target=receivemessage)
receive_thread.start()
