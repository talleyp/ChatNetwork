import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def get_users(user_file):
    with open(user_file,'r') as u_f:
        user_soup = u_f.read()
        users = user_soup.split('\n')
    return users

def test_line(G, line, users):
    weight_inc = 1
    try:
        timestamp, text = line.split('] ',1)
    except ValueError:
        return
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
            G.add_edge(sender,word,weight=new_weight)#,date=datetime.now())

def clean_edges(G):
    time_treshhold = 1
    cur_g = G
    for edge in list(cur_g.edges()):
        edge_time = cur_g.get_edge_data(*edge)['date']
        delta = datetime.now() - edge_time
        if delta > timedelta(minutes=1):
            G.remove_edge(*edge)


if __name__ == "__main__":
    out_file = 'data/soda.gml'
    in_file = 'data/soda_twitch'
    user_file = 'data/soda_users'

    G = nx.DiGraph()
    n = 0
    clean = False
    users = get_users(user_file):
    with open(in_file,'r') as l_f:
        for line in l_f:
            if n>100:
                clean_edges(G)
                n = 0
            test_line(G,line,users)
    nx.write_gml(G,out_file)