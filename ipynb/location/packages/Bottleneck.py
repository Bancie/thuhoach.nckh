from sympy import symbols, Eq, solve
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from packages import ShortestPath

class BottleNeck():
    
    def __init__(self, sourceGraph, vertices, vertex_i, vertex_j, vertex):
        self.sourceGraph = sourceGraph
        self.vertices = vertices
        self.vertex_i = vertex_i
        self.vertex_j = vertex_j
        self.vertex = vertex
        
    def distance(self, src, dest):
        a = ShortestPath.Graph(self.vertices)
        a.graph = self.sourceGraph
        path, distance = a.getShortestPath(ord(src) - 65, ord(dest) - 65)
        return distance
        
    def alpha(self):
        x = symbols('x')
        equation = Eq(x * self.distance(self.vertex_i, self.vertex_j) + self.distance(self.vertex_i, self.vertex), (1-x)*self.distance(self.vertex_i, self.vertex_j) + self.distance(self.vertex_j, self.vertex))
        return solve(equation, x)

# ----------------TEST CASE------------------

graph = [[0, 4, 0, 0, 0, 0, 0, 8, 0],
           [4, 0, 8, 0, 0, 0, 0, 11, 0],
           [0, 8, 0, 7, 0, 4, 0, 0, 2],
           [0, 0, 7, 0, 9, 14, 0, 0, 0],
           [0, 0, 0, 9, 0, 10, 0, 0, 0],
           [0, 0, 4, 14, 10, 0, 2, 0, 0],
           [0, 0, 0, 0, 0, 2, 0, 1, 6],
           [8, 11, 0, 0, 0, 0, 1, 0, 7],
           [0, 0, 2, 0, 0, 0, 6, 7, 0]
           ]

a = infoma(graph, 9, 'A', 'B', 'C')

# print(a.distance('A', 'B'))
print(a.alpha())