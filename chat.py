from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time


host = '127.0.0.1'
port = 5000
bufsiz = 1024
addr = (host, port)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(addr)


def receive():
    while True:
        try:
            msg = client_socket.recv(bufsiz).decode("utf-8")
            print(msg)
        except OSError:
            break


def send():
    time.sleep(0.2)
    msg = input()
    if msg != '{q}':
        client_socket.send(bytes(msg, "utf-8"))
    else:
        client_socket.send(bytes(msg, "utf-8"))
        client_socket.close()
        exit()


if __name__ == "__main__":
    receive_thread = Thread(target=receive)
    receive_thread.start()
    while True:
        send()
