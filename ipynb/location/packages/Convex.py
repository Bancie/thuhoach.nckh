import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations

def ConvexHull(points):
    
    points = sorted(set(points))

    if len(points) <= 1:
        return points

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    upper = []
    
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    return lower[:-1] + upper[:-1]

class UpperHull:
    
    def __init__(self, lowerBound, points, upperBound):
        self.lower = lowerBound
        self.p = np.array(points)
        self.upper = upperBound
        self.sort = self.p[np.argsort(points[:, 0])]
    
    def is_upper_turn(self, p1, p2, p3):
        return (p2[0]-p1[0])*(p3[1]-p1[1]) - (p2[1]-p1[1])*(p3[0]-p1[0]) < 0
            
    def upper(self, ):
        
        upper_hull = []

        for pt in self.sort:
            while len(upper_hull) >= 2 and not self.is_upper_turn(upper_hull[-2], upper_hull[-1], pt):
                upper_hull.pop()
            upper_hull.append(pt)
        
        return np.array(upper_hull)

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

class LocalMinima:
    
    def __init__(self):
        self.lines = []
    
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
    
    def showVal(self, _lowerBound, _upperBound):
        
        candidates = self.BreakpointList() + [_lowerBound, _upperBound]
        
        min_val = float('inf')
        min_x = None
        
        for x in candidates:
            val = self.upper_envelope(x)
            if val < min_val:
                min_val = val
                min_x = x
        
        return min_val, min_x