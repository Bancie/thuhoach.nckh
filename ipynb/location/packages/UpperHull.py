import numpy as np
import matplotlib.pyplot as plt

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