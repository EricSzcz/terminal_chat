import socket
import time

clients = []

s = socket.socket()
# host = socket.gethostname()
host = '127.0.0.1'
port = 5000
s.bind((host,port))
s.listen(5)

quitting = False
print("Server Started.")
print(host)
print(port)
while not quitting:
    try:
        data, addr = s.accept()
        # print(data.recv(1024).decode('utf-8')) funcionando
        # print(addr)
        # addr = s.accept()
        # data = addr.recv(1024).decode('utf-8')
        if "Quit" in str(data):
            quitting = True
        if addr not in clients:
            clients.append(addr)
            
        print(time.ctime(time.time()) + str(addr) + ": :" + str(data.recv(1024).decode('utf-8')))
        message = data.recv(1024).decode('utf-8')
        for client in clients:
            s.sendto(message, client)
    except Exception as e:
        print(e)        
s.close()