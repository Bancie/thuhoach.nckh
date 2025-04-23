import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

class Graph():
    
    def __init__(self, src):
        self.src = np.array(src)
        self.marked_points = []
        
    def show(self):
        G = nx.from_numpy_array(self.src)
        mapping = {i: chr(65 + i) for i in G.nodes}
        G = nx.relabel_nodes(G, mapping)
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1500, font_weight='bold')
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        plt.show()
    
    def show_node(self, show_marks=True):
        G = nx.from_numpy_array(self.src)
        mapping = {i: f'v{i+1}' for i in G.nodes}
        G = nx.relabel_nodes(G, mapping)
        self.G = G
        self.pos = nx.spring_layout(G)
        nx.draw(G, self.pos, with_labels=True, node_color='skyblue', node_size=1500, font_weight='bold')
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, self.pos, edge_labels=edge_labels)

        if show_marks:
            for u, v, alpha, label, color in self.marked_points:
                if u in self.pos and v in self.pos:
                    x1, y1 = self.pos[u]
                    x2, y2 = self.pos[v]
                    x = (1 - alpha) * x1 + alpha * x2
                    y = (1 - alpha) * y1 + alpha * y2
                    plt.plot(x, y, 'o', color=color)
                    plt.annotate(label, (x, y), textcoords="offset points", xytext=(10, 10), ha='center')

        plt.show()

    def add_marked_point_on_edge(self, u, v, alpha=0.5, label='x', color='red'):
        """
        Add a point to be marked on edge (u, v) at position alpha.
        """
        self.marked_points.append((u, v, alpha, label, color))