import socket
import threading
# import argparse

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = "DC"

'''argParser = argparse.ArgumentParser(description='Start the chat server and listen for incoming connections.')
args = argParser.parse_args()'''


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
clients = []


def broadcast(message, conn):
    for i in clients:
        if i is not conn:
            i.send(message)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    while True:
        msg = conn.recv(2048).decode(FORMAT)
        broadcast(msg.encode(FORMAT), conn)
        if msg == DISCONNECT_MSG:
            broadcast(f'\nUser is now disconnected from chat room\n'.encode(FORMAT), conn)
            clients.remove(conn)
            break
        if msg == "connect ola":
            ola(msg, conn)
        if msg == "connect seb":
            seb(msg, conn)
        if msg == "connect fred":
            fred(msg, conn)
        if msg == "connect haakon":
            haakon(msg, conn)

        print(f"[{addr}] {msg}")
    conn.close()


def ola(msg, conn):
    broadcast("Vinland saga", conn)


def seb(msg, conn):
    broadcast()


def fred(msg, conn):
    broadcast()


def haakon(msg, conn):
    broadcast()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")
        clients.append(conn)


print("[STARTING] server is starting...")
start()
