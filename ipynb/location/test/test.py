import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from packages.ortool import data_model

import numpy as np

def generate_transport_cost_matrix(n, low, high):
    matrix = np.random.randint(low, high, size=(n, n))
    np.fill_diagonal(matrix, 0)
    return matrix

cost_matrix = generate_transport_cost_matrix(50, 1, 100).tolist()
print(cost_matrix)
# cost_matrix = [[0, 17, 4, 42, 90, 41, 31, 26, 1, 49], [23, 0, 51, 53, 4, 69, 97, 21, 63, 81], [78, 61, 0, 41, 81, 56, 94, 84, 30, 39], [98, 57, 79, 0, 72, 54, 71, 98, 51, 17], [63, 41, 1, 20, 0, 57, 59, 69, 70, 66], [50, 55, 2, 39, 40, 0, 6, 12, 41, 98], [41, 97, 15, 58, 34, 18, 0, 2, 94, 47], [71, 62, 9, 83, 18, 5, 44, 0, 13, 34], [94, 79, 65, 86, 12, 45, 76, 32, 0, 25], [61, 21, 94, 48, 41, 81, 69, 74, 64, 0]]

print("Cost Matrix:")
for row in cost_matrix:
    print(row)

print("\n")
print("p-Median (p=2):")
print("\n")

df = data_model(
        cost_matrix=cost_matrix,
        p_facility=2
    )

NumVariables, version_solving, obj_val, result, wall_time, iterations, nodes = df.solver(is_maximization=False, is_integer=True)

print(f"Optimal Objective Value: {obj_val}")
for row in result:
    print(row)
print(f"Number of Variables: {NumVariables}")
print(f"Solver Version: {version_solving}")
print(f"Wall Time: {wall_time} ms")
print(f"Iterations: {iterations}")
print(f"Nodes: {nodes}")