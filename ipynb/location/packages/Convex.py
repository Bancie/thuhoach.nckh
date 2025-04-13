import numpy as np
import matplotlib.pyplot as plt


def convex_hull(points):
    """Computes the convex hull of a set of 2D points.

    Input: an iterable sequence of (x, y) pairs representing the points.
    Output: a list of vertices of the convex hull in counter-clockwise order,
      starting from the vertex with the lexicographically smallest coordinates.
    Implements Andrew's monotone chain algorithm. O(n log n) complexity.
    """

    # Sort the points lexicographically (tuples are compared lexicographically).
    # Remove duplicates to detect the case we have just one unique point.
    points = sorted(set(points))

    # Boring case: no points or a single point, possibly repeated multiple times.
    if len(points) <= 1:
        return points

    # 2D cross product of OA and OB vectors, i.e. z-component of their 3D cross product.
    # Returns a positive value, if OAB makes a counter-clockwise turn,
    # negative for clockwise turn, and zero if the points are collinear.
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    # Build lower hull 
    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # Build upper hull
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # Concatenation of the lower and upper hulls gives the convex hull.
    # Last point of each list is omitted because it is repeated at the beginning of the other list. 
    return lower[:-1] + upper[:-1]

# Example: convex hull of a 10-by-10 grid.
assert convex_hull([(i//10, i%10) for i in range(100)]) == [(0, 0), (9, 0), (9, 9), (0, 9)]


# UPPER ENVELOPES

class UpperEnv:
    
    def __init__(self, lowerBound, points, upperBound):
        self.lower = lowerBound
        self.p = np.array(points)
        self.upper = upperBound
        self.sort = self.p[np.argsort(points[:, 0])]
    
    def is_upper_turn (self, p1, p2, p3):
        # Cross product: negative means upper turn
        return (p2[0]-p1[0])*(p3[1]-p1[1]) - (p2[1]-p1[1])*(p3[0]-p1[0]) < 0
            
    def upper (self, ):
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