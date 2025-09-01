from ortools.linear_solver import pywraplp
import numpy as np

class data_model():
    def __init__(self, cost_matrix, p_facility, constraint_co_leq):
        self.cost_matrix = cost_matrix
        self.p_facility = p_facility
        self.constraint_co_leq = constraint_co_leq
    
    def getRowsCols(self):
        return np.array(self.cost_matrix).shape
    
    def create_data_model(self):
        data = {}
        bounds_eq = []
        rows, cols = np.array(self.cost_matrix).shape
        
        for i in range(rows):
            bounds_eq.append(1)
        bounds_eq.append(self.p_facility)

        constraint_co_eq = np.zeros((rows, rows * cols), dtype=int)
        for i in range(rows):
            start = i * cols
            for j in range(cols):
                constraint_co_eq[i, start + j] = 1
        row = np.zeros(rows * cols, dtype=int)
        for i in range(rows):
            for j in range(cols):
                if i == j:
                    row[i * cols + j] = 1
        constraint_co_eq = np.vstack([constraint_co_eq, row])
        
        num_constraints_leq = 0
        for i in range(rows):
            for j in range(cols):
                if i != j:
                    num_constraints_leq += 1
        
        data["constraint_co_leqeffs_leq"] = self.constraint_co_leq
        
        bounds_leq = np.zeros(num_constraints_leq, dtype=int)
        
        data["bounds_leq"] = bounds_leq

        data["constraint_co_leqeffs_eq"] = constraint_co_eq
        data["bounds_eq"] = bounds_eq
        
        data["obj_coeffs"] = np.array(self.cost_matrix).flatten().tolist()
        data["num_vars"] = np.array(self.cost_matrix).size


        data["num_constraints_leq"] = num_constraints_leq
        
        data["num_constraints_eq"] = rows + 1

        return data
    
    def getNumConstraintsLeq(self):
        rows, cols = np.array(self.cost_matrix).shape
        num_constraints_leq = 0
        for i in range(rows):
            for j in range(cols):
                if i != j:
                    num_constraints_leq += 1
        return num_constraints_leq
    
    def getCostMatrix(self):
        return self.cost_matrix

    def solver(self,is_maximization=True, is_integer=False):
        size = np.array(self.cost_matrix).shape[0]
        data = self.create_data_model()
        result = []
        if is_integer:
            solver = pywraplp.Solver.CreateSolver("SAT")
        else:
            solver = pywraplp.Solver.CreateSolver("GLOP")
            
        if not solver:
            return

        infinity = solver.infinity()
        
        x = {}
        
        if is_integer:
            for j in range(data["num_vars"]):
                x[j] = solver.NumVar(0, infinity, "x[%i]" % j)
            NumVariables = solver.NumVariables()
        else:
            for j in range(data["num_vars"]):
                x[j] = solver.IntVar(0, infinity, "x[%i]" % j)
            NumVariables = solver.NumVariables()

        for i in range(data['num_constraints_leq']):
            constraint_expr = [data['constraint_co_leqeffs_leq'][i][j] * x[j] for j in range(data['num_vars'])]
            solver.Add(sum(constraint_expr) <= data['bounds_leq'][i])
            
        for i in range(data['num_constraints_eq']):
            constraint_expr = [data['constraint_co_leqeffs_eq'][i][j] * x[j] for j in range(data['num_vars'])]
            solver.Add(sum(constraint_expr) == data['bounds_eq'][i])

        objective = solver.Objective()
        for j in range(data["num_vars"]):
            objective.SetCoefficient(x[j], data["obj_coeffs"][j])
        if is_maximization:
            objective.SetMaximization()
        else:
            objective.SetMinimization()

        version_solving = solver.SolverVersion()
        status = solver.Solve()

        if is_integer:
            if status == pywraplp.Solver.OPTIMAL:
                obj_val = solver.Objective().Value()
                
                for i in range(size):
                    row_vals = []
                    for j in range(size):
                        idx = i * size + j
                        row_vals.append(x[idx].solution_value())
                    result.append(row_vals)

                wall_time = solver.wall_time()
                iterations = solver.iterations()
                nodes = solver.nodes()
                return NumVariables, version_solving, obj_val, result, wall_time, iterations, nodes
            else:
                print("The problem does not have an optimal solution.")
        else:
            if status == pywraplp.Solver.OPTIMAL:
                obj_val = solver.Objective().Value()
                
                for i in range(size):
                    row_vals = []
                    for j in range(size):
                        idx = i * size + j
                        row_vals.append(x[idx].solution_value())
                    result.append(row_vals)

                wall_time = solver.wall_time()
                iterations = 0
                nodes = 0
                return NumVariables, version_solving, obj_val, result, wall_time, iterations, nodes
            else:
                print("The problem does not have an optimal solution.")