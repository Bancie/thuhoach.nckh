from multipledispatch import dispatch
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
from sympy import symbols, Eq, solve
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from packages import ShortestPath

class FunctionPlotter:

    def __init__(self, lowerbound, upperbound, num_points):
        self.x_range = (lowerbound, upperbound)
        self.num_points = num_points
        self.functions = []
        self.labels = []
        self.x = np.linspace(self.x_range[0], self.x_range[1], self.num_points)

    def add_function(self, func, label):
        self.functions.append(func)
        self.labels.append(label)

    def plot(self, title="Function Plot", xlabel="x", ylabel="y"):
        
        plt.figure(figsize=(10, 6))
        
        for func, label in zip(self.functions, self.labels):
            y = func(self.x)
            plt.plot(self.x, y, label=label)

        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()
        plt.grid(True)
        plt.axhline(0, color='black', linewidth=0.5)
        plt.axvline(0, color='black', linewidth=0.5)
        plt.show()

class Local:

    def __init__(self, sourceGraph, vertices, vertex_i, vertex_j):
        self.sourceGraph = sourceGraph
        self.vertices = vertices
        self.vertex_i = vertex_i
        self.vertex_j = vertex_j

    @dispatch(str, str)
    def distance(self, src, dest):
        a = ShortestPath.Graph(self.vertices)
        a.graph = self.sourceGraph
        path, distance = a.getShortestPath(ord(src) - 65, ord(dest) - 65)
        return distance

    @dispatch(int, int)
    def distance(self, src, dest):
        a = ShortestPath.Graph(self.vertices)
        a.graph = self.sourceGraph
        path, distance = a.getShortestPath(src, dest)
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

class LocalMinima(Local):

    def __init__(self, sourceGraph, vertices, vertex_i, vertex_j):
        super().__init__(sourceGraph, vertices, vertex_i, vertex_j)
        self.lines = []

    def lowerlm(self, A):
        return self.distance(self.vertex_i, A)

    def upperlm(self, A):
        return self.distance(self.vertex_j, A) + (1-self.distance(self.vertex_i, self.vertex_j))*self.distance(self.vertex_i, self.vertex_j)

    def BoundedValue(self, x):
        i = 0
        val = 0
        while i < self.vertices:
            if i == self.vertex_i:
                i += 1
                continue
            else:
                if x == 'upper':
                    if self.upperlm(i) > val:
                        val = self.upperlm(i)
                elif x == 'lower':
                    if self.lowerlm(i) > val:
                        val = self.lowerlm(i)
            i += 1
        return val
        
    def add_line(self, new_func):
        """
        Add a new function to the list of lines.

        Parameters
        ----------
        new_func : Callable[[float], float]
            A function that takes a float and returns a float.

        Returns
        -------
        None

        Examples
        --------
        >>> lm = LocalMinima()
        >>> lm.add_line(lambda x: x**2)
        >>> lm.lines 
        4
        """
        self.lines.append(new_func)

    def show_lines(self, x=0):
        """
        Prints the output of each stored function evaluated at a given x value.

        Args:
            x (float, optional): The input value to evaluate all functions at. Default is 0.

        Example:
            >>> lm = LocalMinima()
            >>> lm.add_line(lambda x: x + 1)
            >>> lm.show_lines(x=2)
            Line 0: f(2) = 3
        """
        for i, func in enumerate(self.lines):
            try:
                result = func(x)
                print(f"Line {i}: f({x}) = {result}")
            except Exception as e:
                print(f"Line {i}: Error evaluating function - {e}")

    def upper_envelope(self, x):
        return max(f(x) for f in self.lines)

    def intersect(self, f1, f2):
        a1 = f1(1) - f1(0)
        b1 = f1(0)
        a2 = f2(1) - f2(0)
        b2 = f2(0)
        if a1 == a2:
            return None
        return (b2 - b1) / (a1 - a2)

    def BreakpointList(self):
        xs = []
        for f1, f2 in combinations(self.lines, 2):
            x = self.intersect(f1, f2)
            if x is not None:
                xs.append(x)
        return xs

    def lineList(self):
        for i in range(self.vertices):
            if i==self.vertex_i or i==self.vertex_j:
                continue
            else:
                self.add_line(lambda x, i=i:
                    self.distance(i, self.vertex_i) + x * self.distance(self.vertex_i, self.vertex_j)
                )
            
            if i==self.vertex_i or i==self.vertex_j:
                continue
            else:
                self.add_line(lambda x, i=i:
                    self.distance(i, self.vertex_j) + (1 - x) * self.distance(self.vertex_i, self.vertex_j)
                )

    def IntervalValue(self):

        self.lineList()
        
        candidates = self.BreakpointList() + [0, self.distance(self.vertex_i, self.vertex_j)]
        
        min_val = float('inf')
        min_x = None
        
        for x in candidates:
            val = self.upper_envelope(x)
            if val < min_val:
                min_val = val
                min_x = x
        
        return min_val, min_x

    def LocalMinima(self):
        local = []
        local.append(self.BoundedValue('upper'))
        local.append(self.BoundedValue('lower'))
        interval_min_val, _ = self.IntervalValue()
        local.append(interval_min_val)
        return min(local)