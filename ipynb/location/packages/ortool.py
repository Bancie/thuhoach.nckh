from ortools.linear_solver import pywraplp

class programing_sovler():
    def __init__(self, obj_coeffs, constraint_co_leq, bounds_leq, constraint_co_eq, bounds_eq, num_vars, num_constraints_leq, num_constraints_eq):
        self.obj_coeffs = obj_coeffs
        self.constraint_co_leq = constraint_co_leq
        self.bounds_leq = bounds_leq
        self.constraint_co_eq = constraint_co_eq
        self.bounds_eq = bounds_eq
        self.num_vars = num_vars
        self.num_constraints_leq = num_constraints_leq
        self.num_constraints_eq = num_constraints_eq
        
    def create_data_model(self):
        data = {}
        data["constraint_co_leqeffs_leq"] = self.constraint_co_leq
        data["bounds_leq"] = self.bounds_leq

        data["constraint_co_leqeffs_eq"] = self.constraint_co_eq
        data["bounds_eq"] = self.bounds_eq
        
        data["obj_coeffs"] = self.obj_coeffs
        data["num_vars"] = self.num_vars

        data["num_constraints_leq"] = self.num_constraints_leq
        
        data["num_constraints_eq"] = self.num_constraints_eq

        return data

    def integer_solve(self):
        data = self.create_data_model()
        solver = pywraplp.Solver.CreateSolver("SCIP")
        if not solver:
            return

        infinity = solver.infinity()
        x = {}
        for j in range(data["num_vars"]):
            x[j] = solver.IntVar(0, infinity, "x[%i]" % j)
        print("Number of variables =", solver.NumVariables())

        for i in range(data['num_constraints_leq']):
            constraint_expr = [data['constraint_co_leqeffs_leq'][i][j] * x[j] for j in range(data['num_vars'])]
            solver.Add(sum(constraint_expr) <= data['bounds_leq'][i])
            
        for i in range(data['num_constraints_eq']):
            constraint_expr = [data['constraint_co_leqeffs_eq'][i][j] * x[j] for j in range(data['num_vars'])]
            solver.Add(sum(constraint_expr) == data['bounds_eq'][i])

        objective = solver.Objective()
        for j in range(data["num_vars"]):
            objective.SetCoefficient(x[j], data["obj_coeffs"][j])
        objective.SetMaximization()

        print(f"Solving with {solver.SolverVersion()}")
        status = solver.Solve()

        if status == pywraplp.Solver.OPTIMAL:
            print("Objective value =", solver.Objective().Value())
            for j in range(data["num_vars"]):
                print(x[j].name(), " = ", x[j].solution_value())
            print()
            print(f"Problem solved in {solver.wall_time():d} milliseconds")
            print(f"Problem solved in {solver.iterations():d} iterations")
            print(f"Problem solved in {solver.nodes():d} branch-and-bound nodes")
        else:
            print("The problem does not have an optimal solution.")