import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time 
import json
import os

class GraphMaker:
    def __init__(self):    
        self.G = nx.DiGraph()
        websocket.enableTrace(True)#True)
        ws = websocket.WebSocketApp("ws://destiny.gg:9998/ws",
                                on_message = self.on_message,
                                on_error = self.on_error,
                                on_close = self.on_close)
        ws.on_open = self.on_open
        ws.run_forever()

    def get_users(self,message):
        '''On connection get names of all connected users
        This splits those into individuals to have starting point
        '''
        line = message.strip('NAMES ')
        line = json.loads(line)
        self.users = [x['nick'] for x in line["users"]]

    def test_line(self,in_msg):
        '''
        Given a message line test to see if we can find a user
        mentioned to add to the graph. 
        '''
        weight_inc = 1
        line = in_msg.strip('MSG ')
        line = json.loads(line)
        sender = line["nick"]
        message = line["data"]
        if sender not in self.users:
            self.users.append(sender)
        for word in message.split(' '):
            word = word.strip("@") # People will tag with @User 
            if (word in self.users) and (word != sender):
                self.G.add_node(sender)
                self.G.add_node(word)
                new_weight = weight_inc
                if self.G.get_edge_data(sender,word):
                    new_weight = self.G.get_edge_data(sender,word)['weight'] + weight_inc
                self.G.add_edge(sender,word,weight=new_weight,date=datetime.now())
                now = datetime.now()
                if now.minute == 47:
                    self.clean_edges()
                if now.minute == 48:
                    file_name = "data/thread_out_%s_%s_%s.gpickle" % (now.year, now.day, now.hour)
                    if not os.path.exists(file_name):
                        nx.write_gpickle(self.G,file_name)

    def clean_edges(self):
        cur_g = self.G
        for edge in list(cur_g.edges()):
            edge_time = cur_g.get_edge_data(*edge)['date']
            delta = datetime.now() - edge_time
            if delta > timedelta(hours=12):
                self.G.remove_edge(*edge)

    def on_message(self, ws, message):
        if "NAMES" in message:
            self.get_users(message)
        if "MSG" in message:
            self.test_line(message)

    def on_error(self, ws, error):
        print("error: %s" % error)

    def on_close(self, ws):
        print("### closed ###")

    def on_open(self, ws):
        def run(*args):
            for i in range(30000):
                time.sleep(1)
                #ws.send("Hello %d" % i)
            time.sleep(1)
            ws.close()
            print("thread terminating...")
        thread.start_new_thread(run, ())

if __name__ == "__main__":
    GraphMaker()