from socket import AF_INET, socket, SOCK_STREAM
import threading
import os
import time
import subprocess
import signal

clients = {}
addresses = {}
path = os.getcwd()

host = '127.0.0.1'
port = 5000
bufsize = 1024
addr = (host, port)
server = socket(AF_INET, SOCK_STREAM)
server.bind(addr)


class Server(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

        self.shutdown_flag = threading.Event()


    def accept_incoming_connections(self):
        while not self.shutdown_flag.is_set():
            try:
                client, client_address = server.accept()
                print("%s:%s has connected," % client_address)
                client.send(bytes("welcome, type your name and press enter! \n or type '{q}' to Exit", "utf-8"))
                addresses[client] = client_address
                threading.Thread(target=self.handle_client, args=(client,)).start()
            except OSError:
                break


    def handle_client(self, client):
        name = client.recv(bufsize).decode("utf-8")
        msg = "%s has joined the chat!" % name
        self.broadcast(bytes(msg, "utf-8"))
        clients[client] = name
        while not self.shutdown_flag.is_set():
            try:
                msg = client.recv(bufsize)
                if msg != bytes("{q}", "utf-8"):
                    self.broadcast(msg, name+": ")
                else:
                    client.send(bytes("{q}", "utf-8"))
                    client.close()
                    del clients[client]
                    self.broadcast(bytes("%s has left the chat." % name, "utf-8"))
                    break
            except OSError:
                break


    def broadcast(self, msg, prefix=""):
        for sock in clients:
            sock.send(bytes(prefix, "utf-8")+msg)
        fifo = open(path+'/myfifo.fifo', "w")
        fifo.write("%s\n" %msg)
        fifo.close()

class ServerExit(Exception):
    pass

def handler(signum, stack):
    print('Caught signal %d' % signum)
    raise ServerExit

def main():

    try:
        server.listen(5)
        os.mkfifo(path+'/myfifo.fifo')
        proc = subprocess.Popen(['sudo python3 logger.py', '', '...'], shell=True)
        pid = proc.pid

        signal.signal(signal.SIGTERM, handler)
        signal.signal(signal.SIGINT, handler)

        print("Waiting for connection...")
        print("Type 'ctrl + c' to stop the server")
    
        srv = Server()
        srv.accept_incoming_connections()

        while True:
            time.sleep(0.5)

    except ServerExit:
        srv.shutdown_flag.set()
        os.kill(pid, signal.SIGKILL)
        os.unlink(path+'/myfifo.fifo')
        os._exit(0)

    print('Exiting Server...')

if __name__ == "__main__":
    main()
