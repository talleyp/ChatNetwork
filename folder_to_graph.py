import networkx as nx
import matplotlib.pyplot as plt
import pickle
from datetime import datetime, timedelta
from os import listdir
from os.path import isfile, join
import re

def get_users(user_file):
    with open(user_file,'r') as u_f:
        user_soup = u_f.read()
        users = user_soup.split('\n')
    users = [x.lower() for x in users]
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

def test_line(G_complete, G_temp, line, users, msg_count, time_users):
    try:
        timestamp, text = line.split('] ',1)
    except ValueError:
        return (G_complete, G_temp, msg_count,time_users)
    dt_timestamp = datetime.strptime(timestamp, "[%Y-%m-%d %H:%M:%S %Z")
    str_timestamp = dt_timestamp.strftime("%Y-%m-%d %H:%M:%S")

    try:
        sender, message = text.split(': ',1)
    except ValueError:
        return (G_complete, G_temp, msg_count,time_users)
    if sender not in users:
        users.append(sender)
    to_self = True
    for word in message.split(' '):
        # Try and find if the user sent a message to someone
        word = re.sub('[@]', '', word)
        word = word.lower()
        if (word in users) and (word != sender):
            to_self = False
            G_complete = update_graph(G_complete, sender, word)
            G_temp = update_graph(G_temp, sender, word)
            time_users.add(word)
    if to_self:
        # If the line was not directed, treat as though it was for the sender only
        G_temp = update_graph(G_temp, sender, sender)
        msg_count = msg_count+1
    return (G_complete, G_temp, msg_count, time_users)

def clean_edges(G):
    time_treshhold = 1
    cur_g = G
    for edge in list(cur_g.edges()):
        edge_time = cur_g.get_edge_data(*edge)['date']
        delta = datetime.now() - edge_time
        if delta > timedelta(minutes=1):
            G.remove_edge(*edge)

def component_analysis(G):
    '''Find distribution of size of componenets, and their average degree within the component'''
    n_com = nx.number_connected_components(G) # number of components
    n_node_dist = [] # number of nodes within each component
    avg_deg_dist = [] # average degree for each component
    for c in nx.connected_components(G):
        n_node_dist.append(len(c))
        temp_avg = 0
        for node in c:
            temp_avg = temp_avg + G.degree[node]
        avg_deg_dist.append(temp_avg/len(c))
    return (avg_deg_dist, n_node_dist)

def lonely_people(G):
    '''Find people who speak to someone else and get the amount they respond back'''
    pls_respond = {}
    for edge in G.edges():
        n0 = edge[0]
        n1 = edge[1]
        if n1 != n0:
            w0 = G.get_edge_data(n0,n1)['weight']
            try:
                w1 = G.get_edge_data(n1,n0)['weight']
            except TypeError:
                w1=0
            diff = w1-w0
            if diff > 0:
                dic_edge = (n1,n0)
            else:
                dic_edge = (n0,n1)
            if ((n0,n1) not in pls_respond) and ((n1,n0) not in pls_respond):
                pls_respond[dic_edge] = abs(diff)
    max_n = 9
    n=0
    for key, value in sorted(pls_respond.items(), key=lambda item: (item[1], item[0]),reverse=True):
        print("%s: %s" % (key, value))
        if n > max_n:
            break
        n+=1
    return pls_respond

def sociability(G):
    '''Compare number of messages sent to no one to number sent at someone'''
    soc = {}
    for node in G.nodes():
        try:
            n_self = G.get_edge_data(node,node)['weight']
        except TypeError:
            n_self = 0
        n_out = 0
        for neighbor in nx.all_neighbors(G,node):
            if neighbor != node:
                try:
                    n_out = n_out + G.get_edge_data(node,neighbor)['weight']
                except TypeError:
                    pass
        if (n_out+n_self) > 0:
            soc[node] = n_self/(n_out+n_self)
    return soc

def basics(G):
    '''Not custom measurements'''
    rec = nx.reciprocity(G) # likelihood of vertices in a directed network to be mutually linked
    rich_club = nx.rich_club_coefficient(G)
    return (rec, rich_club)

def time_analysis(line,prev_hour,ns_cnt,msg_count,soc_ts,time_users):
    try:
        timestamp, text = line.split('] ',1)
    except ValueError:
        return (prev_hour, ns_cnt, msg_count, soc_ts,time_users)
    dt_timestamp = datetime.strptime(timestamp, "[%Y-%m-%d %H:%M:%S %Z")
    str_timestamp = dt_timestamp.strftime("%Y-%m-%d %H:%M:%S")
    if dt_timestamp.hour != prev_hour:
        hour_soc = 1 - (ns_cnt / msg_count)
        rate = msg_count / 60
        unq_users = len(time_users)
        soc_ts[dt_timestamp] = {"soc":hour_soc,"rate":rate,"n_user":unq_users}

        if prev_hour==23:
            prev_hour=-1
        else:
            prev_hour = dt_timestamp.hour
        time_users.clear()
        msg_count = 0
        ns_cnt = 0
    return (prev_hour, ns_cnt, msg_count, soc_ts,time_users)

if __name__ == "__main__":
    out_graph = 'data/sodapoppin/sodapoppin.gml'
    out_graph_with_self = 'data/sodapoppin/sodapoppin_self.gml'
    out_ts = 'data/sodapoppin/sodapoppin_ts.p'
    log_folder = 'data/sodapoppin/logs/'
    user_file = 'data/sodapoppin/users.txt'

    G_full = nx.DiGraph()
    G_temp = nx.DiGraph()
    prev_hour = -1
    soc_ts = {}
    counter = 0
    non_soc = 0
    time_users = set([])
    users = get_users(user_file)
    for f in listdir(log_folder):
        print(f)
        in_file = log_folder+f
        with open(in_file,'r') as l_f:
            for line in l_f:
                if isinstance(line, str):
                    counter = counter + 1
                    #print(non_soc_counter)
                    prev_hour,non_soc,counter,soc_ts,time_users = time_analysis(line,prev_hour,\
                                                                        non_soc,counter,\
                                                                        soc_ts,time_users)
                    G_full, G_temp, non_soc,time_users = test_line(G_full,G_temp,\
                                                                        line,users,\
                                                                        non_soc,time_users)
    nx.write_gml(G_full,out_graph)
    nx.write_gml(G_temp,out_graph_with_self)
    pickle.dump( soc_ts, open( out_ts, "wb" ) )