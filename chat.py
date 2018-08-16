from socket import AF_INET, socket, SOCK_STREAM
import threading
import time
import signal
import os


host = '127.0.0.1'
port = 5000
bufsiz = 1024
addr = (host, port)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(addr)


def receive():
    while not shutdown_flag.is_set():
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


class ChatExit(Exception):
    pass


def handler(signum, stack):
    print('Caught signal %d' % signum)
    raise ChatExit


if __name__ == "__main__":
    try:
        signal.signal(signal.SIGTERM, handler)
        signal.signal(signal.SIGINT, handler)
        shutdown_flag = threading.Event()

        receive_thread = threading.Thread(target=receive)
        receive_thread.start()
        while not shutdown_flag.is_set():
            send()
    except ChatExit:
        client_socket.send(bytes('{q}', "utf-8"))
        client_socket.close()
        shutdown_flag.set()
        os._exit(0)
