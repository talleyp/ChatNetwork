import networkx as nx
from datetime import datetime

time_treshhold = 1
for edge in G.edges():
    edge_time = G.get_edge_data(*edge)['date']
    delta = datetime.now() - edge_time
    if delta.hours > 1:
        G.remove_edge(*edge)
