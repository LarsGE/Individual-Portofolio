#Portofolio-1 Lars Grotnes Edvardsen s351924

import socket,threading,time,sys,argparse

#Parsing to check that the necessary arguments are provided
parser = argparse.ArgumentParser(description='')
parser.add_argument('port', type=int, help='')
args = parser.parse_args()
port = args.port

#The server socket with a list of all clients and their names
serverS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverS.bind(('localhost', port))
serverS.listen()
clients = []
clientNames = []

#Client broadcasting a message to other clients
def messageClients(message, client):
    for i in clients:
        #No message back to sender
        if i is not client:
            i.send(message)


#Chatting between host and bots
def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            msg = message.decode().split(": ")

            if (msg[1] == "SHUTDOWN"):
                time.sleep(1)
                print("Disconnecting clients")
                for i in clients:
                    i.close()
                print("Server status: Down\nStopped listening to connections...")
                exit()

            else:
                time.sleep(0.5)
                messageClients(message, client)  #Message to all bots

        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            name = clientNames[index]
            messageClients(f'{name} has disconnected from the chat room!'.encode('utf-8'), client)
            print(f'{name} disconnected from the chat room')
            clientNames.remove(name)
            break

#Connect clients to the chat and set server status
def receive():
    print('\nServer status: Running\nListening to connections...\n')
    while True:
        client, address = serverS.accept()

        client.send('name?'.encode('utf-8'))
        name = client.recv(1024).decode('utf-8')
        clientNames.append(name)
        clients.append(client)
        print(f'Successfully established a connection with {name} {str(address)}')
        messageClients(f'{name} has connected to the chat room'.encode('utf-8'), client)
        client.send('You are now connected to the chat room!'.encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

receive()