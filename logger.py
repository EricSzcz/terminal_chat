import os
import sys
import time


def listener():
	path = os.getcwd()+'/'
	fifo = open(path+'/myfifo.fifo', "r")
	for line in fifo:
		f = open("chat_log", "a+")
		f.write(time.ctime()+line)
		f.close()
	fifo.close()


if __name__ == "__main__":
	try:
		print('logger is running...')
		while True:
			listener()
	except:
		os._exit(0)


