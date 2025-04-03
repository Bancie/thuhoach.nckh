from sympy import symbols, Eq, solve
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from packages import ShortestPath

class BP():
    
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