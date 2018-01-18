import cfg
import socket
import re
import time
import thread
from time import sleep

def main():
	s = socket.socket()
	s.connect((cfg.HOST,cfg.PORT))
	s.send("PASS {}\n\n".format(cfg.PASS).encode("utf-8"))
	s.send("NICK {}\n\n".format(cfg.NICK).encode("utf-8"))
	s.send("JOIN {}\n\n".format(cfg.CHAN).encode("utf-8"))

	while True:
		response = s.recv(1024).decode("utf-8")
		print(response)
		if response == "PING"

if __name__ == '__main__': main()