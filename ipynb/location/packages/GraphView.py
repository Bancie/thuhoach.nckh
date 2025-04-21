import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

class Graph():
    
    def __init__(self, src):
        self.src = np.array(src)
        
    def show(self):
        G = nx.from_numpy_array(self.src)
        mapping = {i: chr(65 + i) for i in G.nodes}
        G = nx.relabel_nodes(G, mapping)
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1500, font_weight='bold')
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        plt.show()
    
    def show_node(self):
        G = nx.from_numpy_array(self.src)
        mapping = {i: f'v{i+1}' for i in G.nodes}
        G = nx.relabel_nodes(G, mapping)
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1500, font_weight='bold')
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        plt.show()