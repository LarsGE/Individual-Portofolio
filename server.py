
import socket
import threading
import argparse

FORMAT = 'utf-8'
DISCONNECT_MSG = "DC"

argParser = argparse.ArgumentParser(description='Start the chat server and listen for incoming connections.')
argParser.add_argument('port', type=int, help='The port the server is running on (Integers only).')
args = argParser.parse_args()
port = args.port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', port))
server.listen()
clients = []
clientNames = []


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

        print(f"[{addr}] {msg}")
    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening...")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")
        clients.append(conn)


print("[STARTING] server is starting...")
start()
