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
        with open('data/user_list','r') as u_f:
            user_soup = u_f.read()
            users = user_soup.split('\n')
        return users

    def test_line(self, line):
        weight_inc = 0.1
        timestamp, text = line.split('] ',1)
        sender, message = text.split(': ',1)
        if sender not in self.users:
            self.users.append(sender)
        for word in message.split(' '):
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
    color_map = {1:'#f09494', 2:'#eebcbc', 3:'#72bbd0', 4:'#91f0a1', 5:'#629fff', 6:'#bcc2f2',  
             7:'#eebcbc', 8:'#f1f0c0', 9:'#d2ffe7', 10:'#caf3a6', 11:'#ffdf55', 12:'#ef77aa', 
             13:'#d6dcff', 14:'#d2f5f0'} 

    plt.figure(figsize=(25,25))
    options = {
        'edge_color': '#FFDEA2',
        'width': 1,
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
    nx.draw(G, node_color=sizes, node_size=sizes, pos=nx.spring_layout(G, k=0.25, iterations=50), **options)
    ax = plt.gca()
    ax.collections[0].set_edgecolor("#555555") 
    plt.show()
                
if __name__ == "__main__":
    G = nx.DiGraph()
    n = 0
    clean = False
    with open('data/example_log','r') as l_f:
        for line in l_f:
            if n>10:
                clean=True
            ChatNetwork(G,line,clean)
            clean=False
            n = n+1
    viz_graph(G)
