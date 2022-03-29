#Portofolio-1 Lars Grotnes Edvardsen s351934

import socket,threading,time,sys,argparse,random

bots = ["Ola", "Seb", "Fred"]

#Parsing to check that the necessary arguments are provided
argPars = argparse.ArgumentParser(description='Connect to the chat room. Example: client.py localhost 1234 Marcus')
argPars.add_argument('IP', type=str, help='IP address of the server the client is connecting to.')
argPars.add_argument('port', type=int, help='The port the client is connecting to.')
argPars.add_argument('name', type=str, help='Client name. Connect as a host or a bot(Ola, Seb or Fred)')
args = argPars.parse_args()
IP = args.IP
port = args.port
name = args.name

clientS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientS.connect((IP, port))

#List of actions, both good and bad
good_things = ["sing", "play", "sprint", "work", "train", "relax"]
bad_things = ["fight", "bicker", "complain", "scream", "kill"]


#Bot functions
def ola(verb):
    if verb in good_things:
        altAns = [
            "{}: Did you say {}? That sounds good!".format(name, verb + "ing"),
            "{}: I think {} would be nice!".format(name, verb + "ing"),
            "{}: At last we can begin {}!".format(name, verb + "ing")
        ]
        return random.choice(altAns)

    elif verb in bad_things:
        altAns2 = [
            "{}: {}? You have lost your mind!".format(name, verb + "ing"),
            "{}: I don't particularly like {}.".format(name, verb + "ing"),
            "{}: Yeah I think I'll pass on {}, sorry.".format(name, verb + "ing")
        ]
        return random.choice(altAns2)

    else:
        return "{}: Sorry, but that's just no fun!".format(name)


def seb(verb):
    altAns3 = [
        "{}: {}...? You must be joking!".format(name, verb + "ing"),
        "{}: {} sounds dull!".format(name, verb + "ing"),
        "{}: I've got more important things to do than {}..".format(name, verb + "ing")
    ]

    if verb in bad_things or verb in good_things:
        return random.choice(altAns3)

    else:
        altAns4 = [
            "{}: Definitely Not doing that.".format(name),
            "{}: You can't expect me to agree to that?".format(name),
            "{}: No!".format(name)
        ]
        return random.choice(altAns4)


def fred(verb):
    if verb in bad_things:
        altAns5 = [
            "{}: {}? I am not agreeing to that.".format(name, verb + "ing"),
            "{}: You know I don't like {}...".format(name, verb + "ing"),
            "{}: {}? Really...".format(name, verb + "ing")
        ]
        return random.choice(altAns5)

    elif verb in good_things:
        altAns6 = [
            "{}: {}?? Sounds good to me".format(name, verb + "ing"),
            "{}: {}, let's do it.".format(name, verb + "ing"),
            "{}: I guess {} isn't to bad.".format(name, verb + "ing")
        ]
        return random.choice(altAns6)

    else:
        return "{}: I am unsure.".format(name)


#Controls the messages received from clients
def clientRec():
    while True:
        msg = clientS.recv(1024).decode('utf-8')

        if msg == "name?":
            clientS.send(name.encode('utf-8'))
        else:
            if ":" in msg:
                msgSplit = msg.split(": ")

                if msgSplit[0] not in bots:
                    v = ""
                    i = 0
                    while i < len(bad_things):
                        if bad_things[i] in msg.lower():
                            v = bad_things[i]

                        if good_things[i] in msg.lower():
                            v = good_things[i]
                        i += 1

                    botmsg = ""

                    if name.lower() == "Ola":
                        botmsg = ola(v)
                    elif name.lower() == "Seb":
                        botmsg = seb(v)
                    elif name.lower() == "Fred":
                        botmsg = fred(v)

                    print(msg)
                    clientSend(botmsg)
                else:
                    time.sleep(0.5)
                    print(msg)
            else:
                print(msg)


def clientSend(msg):
    print(msg)
    clientS.send(msg.encode('utf-8'))


#Host to client message
def clientMsg():
    while True:
        try:
            msg = f'{name}: {input()}'
            split = msg.split(": ")
            if (split[1].isspace() or split[1] == ""):
                print("Can't send an empty string. Please write something!")
                continue
            else:
                time.sleep(0.4)
                print(msg)
                clientS.send(msg.encode('utf-8'))
        except:
            print("\nYou have disconnected from the chat room\n")
            sys.exit()
            break

receive_thread = threading.Thread(target=clientRec)
receive_thread.start()

if name not in bots:
    send_thread = threading.Thread(target=clientMsg)
    send_thread.start()