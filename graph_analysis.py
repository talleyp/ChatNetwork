import Networkx as nx
from datetime import datetime

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

def time_analysis(line,clean_now,ns_cnt,msg_count,soc_ts):
    try:
        timestamp, text = line.split('] ',1)
    except ValueError:
        return
    dt_timestamp = datetime.strptime(timestamp, "[%Y-%m-%d %H:%M:%S %Z")
    str_timestamp = dt_timestamp.strftime("%Y-%m-%d %H:%M:%S")
    if clean_now and dt_timestamp.minute == 0:
        hour_soc = ns_cnt / msg_count
        rate = msg_count / 60
        soc_ts[dt_timestamp] = {"soc":hour_soc,"rate":rate}

        clean_now = False
        msg_count = 0
        ns_cnt = 0
    return (clean_now, ns_cnt, msg_count, soc_ts)
