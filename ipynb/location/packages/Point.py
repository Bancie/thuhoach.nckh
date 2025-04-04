from sympy import symbols, Eq, solve
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from packages import ShortestPath

class Local():
    
    def __init__(self, sourceGraph, vertices, vertex_i, vertex_j):
        self.sourceGraph = sourceGraph
        self.vertices = vertices
        self.vertex_i = vertex_i
        self.vertex_j = vertex_j
        
    def distance(self, src, dest):
        a = ShortestPath.Graph(self.vertices)
        a.graph = self.sourceGraph
        path, distance = a.getShortestPath(ord(src) - 65, ord(dest) - 65)
        return distance
    
    def abstractAlpha(self, A, B):
        x = symbols('x')
        equation = Eq(
            x * self.distance(self.vertex_i, self.vertex_j) + self.distance(self.vertex_i, A), 
            (1 - x) * self.distance(self.vertex_i, self.vertex_j) + self.distance(self.vertex_j, B)
        )
        solution = solve(equation, x)
        
        if solution:
            return float(solution[0].evalf())
        else:
            return None
    
    def BottleNeck(self, A):
        return self.abstractAlpha(A, A)
    
    def EquiPoint(self, A, B):
        if self.abstractAlpha(A, B) > self.distance(self.vertex_i, self.vertex_j) or self.abstractAlpha(A, B) < 0:
            return "Not Placed"
        else:
            return self.abstractAlpha(A, B)