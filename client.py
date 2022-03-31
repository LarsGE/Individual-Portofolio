import socket
import random
import argparse
import threading

# Format and disconnect message
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DC"

# Parser that makes sure the necessary arguments are provided
argParser = argparse.ArgumentParser(description='Connect to chat room.')
argParser.add_argument('IP', type=str, help='IP address of the server the client is connecting to.')
argParser.add_argument('port', type=int, help='The port the client is connecting to.')
argParser.add_argument('name', type=str, help='The name of the client.')
args = argParser.parse_args()
IP = args.IP
port = args.port
name = args.name

# TCP socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, port))

# Bot names
bots = ["ola", "seb", "fred"]

# List of good and bat actions
good_actions = ["laugh", "play", "relax", "read", "train", "sleep"]
bad_actions = ["scream", "fight", "moan", "bicker", "complain", "kill"]


# Bot functions
def ola(verb):
    if verb in good_actions:
        altanswers = [
            "{}: WOW!{} sounds amazing!".format(name,verb + "ing"),
            "{}: I think {} is fantastic!".format(name,verb + "ing"),
            "{}: Let's go {}!".format(name,verb + "ing")
        ]
        return random.choice(altanswers)

    elif verb in bad_actions:
        altanswers2 = [
            "{}: {}?! Are you insane?!".format(name,verb + "ing"),
            "{}: I'm not really into {}, sorry.".format(name,verb + "ing"),
            "{}: I'm can not agree to {}".format(name,verb+"ing")
        ]
        return random.choice(altanswers2)

    else:
        return "{}: Sorry, can you repeat that".format(name)


def seb(verb):
    if verb in good_actions:
        altanswers3 = [
            "{}: {}? Can't complain".format(name,verb + "ing"),
            "{}: {}, can't wait to start".format(name,verb + "ing"),
            "{}: I actually enjoy {}".format(name,verb+"ing")
        ]
        return random.choice(altanswers3)

    elif verb in bad_actions:
        altanswers4 = [
            "{}: NO!".format(name),
            "{}: {}, is not for me.".format(name,verb + "ing"),
            "{}: I think I'll pass on {}".format(name,verb + "ing")
        ]
        return random.choice(altanswers4)


def fred(verb):
    if verb in good_actions:
        altanswers5 = [
            "{}: {}?? I am actually excited about that.".format(name,verb+"ing"),
            "{}: You know i like {}!".format(name,verb + "ing"),
            "{}: {}? I mean it's allright".format(name,verb+"ing")
        ]
        return random.choice(altanswers5)

    elif verb in bad_actions:
        altanswers6 = [
            "{}: {}? I don't like that".format(name,verb+"ing"),
            "{}: {}, if everyone else want's to, im in.".format(name,verb + "ing"),
            "{}: I mean.{} isn't horrible.".format(name,verb+"ing")
        ]
        return random.choice(altanswers6)

    else:
        return "{}: Can you rephrase that".format(name)


# Function that receives the message from the clients
def receivemessage():
    while True:
        message = client.recv(2048).decode(FORMAT)
        print(message)


# Function that sends the message to the clients
def clientsend(msg):
    message = msg.encode(FORMAT)
    client.send(message)


# Function that takes clients input
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

# Threads for the messages and receive functions
message_thread = threading.Thread(target=messages)
message_thread.start()
receive_thread = threading.Thread(target=receivemessage)
receive_thread.start()
