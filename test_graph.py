import networkx as nx
from datetime import datetime

with open('data/user_list','r') as u_f:
    user_soup = u_f.read()
    users = user_soup.split('\n')

G = nx.DiGraph()
weight_inc = 0.1
with open('data/example_log','r') as l_f:
    for line in l_f:
        timestamp, text = line.split('] ',1)
        sender, message = text.split(': ',1)
        if sender not in users:
            users.append(sender)
        for word in message.split(' '):
            if (word in users) and (word != sender):
                G.add_node(sender)
                G.add_node(word)
                new_weight = weight_inc
                if G.get_edge_data(sender,word):
                    new_weight = G.get_edge_data(sender,word)['weight'] + weight_inc
                G.add_edge(sender,word,weight=new_weight,date=datetime.now())

nx.write_gml(G,'data/test_gml.gml')
