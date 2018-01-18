import cfg
import urllib2, json
import time
from time import sleep
import thread

def chat(sock, msg):
	sock.send("PRIVMSG #{} :{}\r\n".format(cfg.CHAN,msg))

