from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

clients = {}
addresses = {}

host = '127.0.0.1'
port = 5000
bufsize = 1024
addr = (host, port)
server = socket(AF_INET, SOCK_STREAM)
server.bind(addr)


def accept_incoming_connections():
    while True:
        client, client_address = server.accept()
        print("%s:%s has connected," % client_address)
        client.send(bytes("welcome, type your name and press enter!", "utf-8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):
    name = client.recv(bufsize).decode("utf-8")
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf-8"))
    clients[client] = name
    while True:
        msg = client.recv(bufsize)
        if msg != bytes("{q}", "utf-8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("{q}", "utf-8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf-8"))
            break


def broadcast(msg, prefix=""):
    for sock in clients:
        sock.send(bytes(prefix, "utf-8")+msg)


if __name__ == "__main__":
    server.listen(5)
    print("Waiting for connection...")
    accept_thread = Thread(target=accept_incoming_connections)
    accept_thread.start()
    accept_thread.join()
    server.close()
