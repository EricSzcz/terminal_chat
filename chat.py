import socket
import threading
import time

tLock = threading.Lock()
shutdown = False

def receving(name, sock):
    while not shutdown:
        try:
            tLock.acquire()
            while True:
                # data, addr = sock.recv(1024).decode('utf-8')
                data, addr = sock.accept()
                # data = sock.recv(1024).decode('utf-8')
                print(data.recv(1024).decode('utf-8'))
        except:
            pass
        finally:
            tLock.release()

host = '127.0.0.1'
port = 5000

server = ('127.0.0.1',5000)

s = socket.socket()
print(host)
print(port)
s.connect((host, port))
# s.setblocking(0)

rT = threading.Thread(target=receving, args=("RecvThread",s))
rT.start()

alias = input("Name: ")
message = input(alias + "-> ")
while message != 'q':
    if message != '':
        message = alias + ": " + message        
        s.sendto(message.encode(), server)
    tLock.acquire()
    message = input(alias + "-> ")
    tLock.release()
    time.sleep(0.2)

shudown = True
rT.join()
s.close()