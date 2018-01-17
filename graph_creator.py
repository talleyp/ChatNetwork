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

def viz_graph(G):
    plt.figure(figsize=(25,25))
    edge_width = [G.get_edge_data(*edge)['weight'] for edge in G.edges()]
    options = {
        'edge_color': '#FFDEA2',
        'width': 0.5,#edge_width,
        'with_labels': True,
        'font_weight': 'regular',
    }
    #colors = [color_map[G.degree[node]] for node in G]
    sizes = [G.degree[node] for node in G]

    """
    Using the spring layout :
    - k controls the distance between the nodes and varies between 0 and 1
    - iterations is the number of times simulated annealing is run
    default k=0.1 and iterations=50
    """
    nx.draw(G, node_color=sizes, node_size=sizes*10, pos=nx.spring_layout(G, k=0.25, iterations=50), **options)
    ax = plt.gca()
    #ax.collections[0].set_edgecolor("#555555")
    plt.show()


def find_cliques(G):
    G2 = G.to_undirected()
    big_cliq=nx.make_max_clique_graph(G2)
    viz_graph(big_cliq)

def lonely_people(G):
    pls_respond = {}
    first_node = True
    for edge in G.edges():
        n0 = edge[0]
        n1 = edge[1]
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
            pls_respond[dic_edge] = int(abs(diff)*10)
    max_n = 9
    n=0
    for key, value in sorted(pls_respond.items(), key=lambda item: (item[1], item[0]),reverse=True):
        print("%s: %s" % (key, value))
        if n > max_n:
            break
        n+=1

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
        #n = n+1
    nx.write_gml(G,out_file)
    #G = nx.read_gml('data/soda.gml')
    #viz_graph(G)
    #NetworkAnalysis(G)
