# This file contains the Gurobi implementation of PLRA and two variants of PM.
# 	For PM-Quadratic, the perturbation function used is f(x) = x - beta * x ^ 2
# 	For PM-Exponential, the perturbation function used is f(x) = 1 - exp(-alpha * x)

def PLRA(instance, maxprob = 1.0):
	# PLRA Gurobi implementation
	# Inputs arguments:
	# 	instance: the input instance
	# 	maxprob:  maximum allowed assignment probability
	# Output: an assignment matrix in nested list
	# Initialize Gurobi solver
	import gurobipy as gp
	solver = gp.Model()
	solver.setParam('OutputFlag', 0)
	# Initialize assignment matrix and objective function
	objective  = 0.0
	assignment = [[0.0 for j in range(instance.nr)] for i in range(instance.np)]
	for i in range(instance.np):
		for j in range(instance.nr):
			x = solver.addVar(lb = 0, ub = maxprob, name = f"{i} {j}")
			assignment[i][j] = x
			objective += x * instance.s[i][j]
	solver.setObjective(objective, gp.GRB.MAXIMIZE)
	# Add ellp & ellr as constraints
	for i in range(instance.np):
		assigned = 0.0
		for j in range(instance.nr):
			assigned += assignment[i][j]
		solver.addConstr(assigned == instance.ellp)
	for j in range(instance.nr):
		load = 0.0
		for i in range(instance.np):
			load += assignment[i][j]
		solver.addConstr(load <= instance.ellr)
	# Run the Gurobi solver
	solver.optimize()
	# Return the resulting matching
	return [[assignment[i][j].X for j in range(instance.nr)] for i in range(instance.np)]

def PMQ(instance, beta = 0.5, maxprob = 1.0):
	# PM-Quadratic Gurobi implementation
	# 	The perturbation function used is f(x) = x - beta * x ^ 2
	# Inputs arguments:
	# 	instance: the input instance
	#   beta:     the parameter used in the perturbation function
	# 	maxprob:  maximum allowed assignment probability
	# Output: an assignment matrix in nested list
	# Initialize Gurobi solver
	import gurobipy as gp
	solver = gp.Model()
	solver.setParam('OutputFlag', 0)
	# Initialize assignment matrix and objective function
	objective  = 0.0
	assignment = [[0.0 for j in range(instance.nr)] for i in range(instance.np)]
	for i in range(instance.np):
		for j in range(instance.nr):
			x = solver.addVar(lb = 0, ub = maxprob, name = f"{i} {j}")
			assignment[i][j] = x
			objective += (x - beta * x * x) * instance.s[i][j]
	solver.setObjective(objective, gp.GRB.MAXIMIZE)
	# Add ellp & ellr as constraints
	for i in range(instance.np):
		assigned = 0.0
		for j in range(instance.nr):
			assigned += assignment[i][j]
		solver.addConstr(assigned == instance.ellp)
	for j in range(instance.nr):
		load = 0.0
		for i in range(instance.np):
			load += assignment[i][j]
		solver.addConstr(load <= instance.ellr)
	# Run the Gurobi solver
	solver.optimize()
	# Return the resulting matching
	return [[assignment[i][j].X for j in range(instance.nr)] for i in range(instance.np)]

def PME(instance, alpha = 1.0, maxprob = 1.0):
	# PM-Exponential Gurobi implementation
	# 	The perturbation function used is f(x) = 1 - exp(-alpha * x)
	#   The objective function is not quadratic, but Gurobi only supports quadratic 
	# 	objectives. Therefore, the successive approximation method is used.
	# Inputs arguments:
	# 	instance: the input instance
	#   alpha:    the parameter used in the perturbation function
	# 	maxprob:  maximum allowed assignment probability
	# Output: an assignment matrix in nested list
	def FinishedPME(instance, current, nextret, eps):
		# Decides whether or not to proceed the successive approximation method
		# Inputs arguments:
		# 	instance: the input instance
		#   current:  the current assignment
		# 	nextret:  the next assignment
		#   eps:      the precision parameter
		# Output: [L infinity distance of current and nextret <= eps]
		for i in range(instance.np):
			for j in range(instance.nr):
				if (abs(current[i][j] - nextret[i][j]) > eps):
					return False
		return True

	def IterationPME(instance, current, alpha, maxprob):
		# One iteration of the successive approximation method
		# Inputs arguments:
		# 	instance: the input instance
		#   current:  the current assignment
		#   alpha:    the parameter used in the perturbation function
		# 	maxprob:  maximum allowed assignment probability
		# Output: the next assignment
		# Initialize Gurobi solver
		import gurobipy as gp
		from numpy import exp
		solver = gp.Model()
		solver.setParam('OutputFlag', 0)
		# Initialize assignment matrix and objective function
		objective  = 0.0
		assignment = [[0.0 for j in range(instance.nr)] for i in range(instance.np)]
		for i in range(instance.np):
			for j in range(instance.nr):
				x = solver.addVar(lb = 0, ub = maxprob, name = f"{i} {j}")
				assignment[i][j] = x
				pos = current[i][j]
				coef = [exp(-alpha * pos), -alpha / 2 * exp(-alpha * pos)]
				# Taylor expansion at pos to the second order
				objective += (coef[0] * (x - pos) + coef[1] * (x - pos) * (x - pos)) * instance.s[i][j]
		solver.setObjective(objective, gp.GRB.MAXIMIZE)
		# Add ellp & ellr as constraints
		for i in range(instance.np):
			assigned = 0.0
			for j in range(instance.nr):
				assigned += assignment[i][j]
			solver.addConstr(assigned == instance.ellp)
		for j in range(instance.nr):
			load = 0.0
			for i in range(instance.np):
				load += assignment[i][j]
			solver.addConstr(load <= instance.ellr)
		# Run the Gurobi solver
		solver.optimize()
		# Return the resulting matching
		return [[assignment[i][j].X for j in range(instance.nr)] for i in range(instance.np)]
	
	# The successive approximation method
	eps = 1e-2
	current = [[0.0 for j in range(instance.nr)] for i in range(instance.np)]
	nextret = IterationPME(instance, current, alpha, maxprob)
	while not FinishedPME(instance, current, nextret, eps):
		current = nextret
		nextret = IterationPME(instance, current, alpha, maxprob)
	return nextret