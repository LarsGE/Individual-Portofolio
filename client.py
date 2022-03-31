import socket
import random
import argparse
import time
import threading


PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DC"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


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
