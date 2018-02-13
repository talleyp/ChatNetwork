import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def get_users(user_file):
    with open(user_file,'r') as u_f:
        user_soup = u_f.read()
        users = user_soup.split('\n')
    return users

def update_graph(G, sender, receiver):
    weight_inc = 1
    G.add_node(sender)
    G.add_node(receiver)
    new_weight = weight_inc
    if G.get_edge_data(sender,receiver):
        new_weight = G.get_edge_data(sender,receiver)['weight'] + weight_inc
    G.add_edge(sender,receiver,weight=new_weight)#,date=datetime.now())
    return G



def test_line(G_complete, G_temp, line, users, msg_count, clean_now):
    try:
        timestamp, text = line.split('] ',1)
    except ValueError:
        return
    dt_timestamp = datetime.strptime(timestamp, "[%Y-%m-%d %H:%M:%S %Z")
    str_timestamp = dt_timestamp.strftime("%Y-%m-%d %H:%M:%S")

    if clean_now and dt_timestamp.minute == 0:
        clean_now = False
        G_temp.clear()
    if dt_timestamp.minute == 1:
        clean_now = True

    sender, message = text.split(': ',1)
    if sender not in users:
        users.append(sender)
    to_self = True
    for word in message.split(' '):
        # Try and find if the user sent a message to someone
        if (word in users) and (word != sender):
            to_self = False
            G_complete = update_graph(G_complete, sender, receiver)
            G_temp = update_graph(G_temp, sender, receiver)
    if to_self:
        # If the line was not directed, treat as though it was for the sender only
        G_temp = update_graph(G_temp, sender, sender)
        msg_count+=1
    return (G_complete, G_temp, clean_now,msg_count)

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

    G_full = nx.DiGraph()
    G_temp = nx.DiGraph()
    clean = False
    soc_ts = {}
    counter = 0
    non_soc_counter = 0
    users = get_users(user_file):
    with open(in_file,'r') as l_f:
        for line in l_f:
            counter += 1
            clean,non_soc_counter,counter,soc_ts = time_analysis(line,clean,non_soc_counter,counter,soc_ts):
            G_full, G_temp, clean, non_soc_counter = test_line(G_full,G_temp,line,users,clean,non_soc_counter)
    nx.write_gml(G_full,out_file)