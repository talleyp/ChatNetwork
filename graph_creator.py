import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class ChatNetwork:
    def __init__(self,old_graph,line,clean=False):
        self.G = old_graph
        self.users = self.get_users()
        self.test_line(line)
        if clean:
            self.clean_edges()

    def get_users(self):
        with open('data/twitch_users','r') as u_f:
            user_soup = u_f.read()
            users = user_soup.split('\n')
        return users

    def test_line(self, line):
        weight_inc = 1
        try:
            timestamp, text = line.split('] ',1)
        except ValueError:
            text = " : "
        sender, message = text.split(': ',1)
        if sender not in self.users:
            self.users.append(sender)
        for word in message.split(' '):
            word = word.strip('@')
            if (word in self.users) and (word != sender):
                self.G.add_node(sender)
                self.G.add_node(word)
                new_weight = weight_inc
                if self.G.get_edge_data(sender,word):
                    new_weight = self.G.get_edge_data(sender,word)['weight'] + weight_inc
                self.G.add_edge(sender,word,weight=new_weight,date=datetime.now())

    def clean_edges(self):
        time_treshhold = 1
        cur_g = self.G#.edges()
        for edge in list(cur_g.edges()):
            edge_time = cur_g.get_edge_data(*edge)['date']
            delta = datetime.now() - edge_time
            if delta > timedelta(minutes=1):
                self.G.remove_edge(*edge)

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

class NetworkAnalysis:
    def __init__(self,given_graph):
        self.G = given_graph
        #self.find_cliques()
        #self.lonely_people()
        self.cool_kidz()

    def find_cliques(self):
        G2 = self.G.to_undirected()
        big_cliq=nx.make_max_clique_graph(G2)
        viz_graph(big_cliq)

    def cool_kidz(self):
        all_deg = G.degree()
        for key, value in sorted(all_deg.items(), key=lambda item: (item[1], item[0]),reverse=True):
            print("%s: %s" % (key, value))
            if n > max_n:
                break
            n+=1

    def lonely_people(self):
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
    G = nx.DiGraph()
    n = 0
    clean = False
    with open('data/twitch_example','r') as l_f:
        for line in l_f:
            if n>10:
                clean=True
            ChatNetwork(G,line,clean)
            clean=False
        #n = n+1
    G_out = G
    for edge in G_out.edges():
        del G[edge[0]][edge[1]]['date']
    nx.write_gml(G,'data/twitch.gml')
    #nx.write_gml(G,'data/weighted.gml')
    #G = nx.read_gml('data/weighted.gml')
    #viz_graph(G)
    #NetworkAnalysis(G)
