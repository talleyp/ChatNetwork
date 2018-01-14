import networkx as nx
from datetime import datetime

class ChatNetwork():
    def __init__(self,old_graph=none):
        if old_graph:
            self.G = old_graph
        else:
            self.G = nx.DiGraph()
        self.users = getUsers()

    def getUsers(self):
        with open('data/user_list','r') as u_f:
            user_soup = u_f.read()
            users = user_soup.split('\n')
        return users

    def testLine(self, line):
        weight_inc = 0.1
        timestamp, text = line.split('] ',1)
        sender, message = text.split(': ',1)
        if sender not in self.users:
            self.users.append(sender)
        for word in message.split(' '):
            if (word in users) and (word != sender):
                self.G.add_node(sender)
                self.G.add_node(word)
                new_weight = weight_inc
                if self.G.get_edge_data(sender,word):
                    new_weight = self.G.get_edge_data(sender,word)['weight'] + weight_inc
                self.G.add_edge(sender,word,weight=new_weight,date=datetime.now())

    def cleanEdges(self)
        time_treshhold = 1
        for edge in self.G.edges():
            edge_time = self.G.get_edge_data(*edge)['date']
            delta = datetime.now() - edge_time
            if delta.hours > 1:
                self.G.remove_edge(*edge)

if name == "__main__":
    with open('data/example_log','r') as l_f:
        for line in l_f:
            
