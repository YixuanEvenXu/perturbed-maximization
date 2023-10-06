# This file contains several utility functions called by the main experiments.

def RunPLRA(instance, datapoints, iters = 10, eps = 1e-4):
	# This function runs PLRA and returns the assigments and hyperparameters of it.
	# For the hyperparameter tuning, the function does binary search to find the
	# smallest Q that satisfies the relative quality requirement.
	# Inputs arguments:
	# 	instance:   the input instance
	# 	datapoints: relative quality requirements
	#   iters:      number of iterations in the binary search
	#   eps:        precision parameter
	# Output:
	#   A list of two lists [maxprobs, assignments]
	#   maxprobs:    hyperparameters used for each relative quality requirement
	#   assignments: assignments for each relative quality requirement
	import metrics
	import algorithms
	ret = [[], []]
	for datapoint in datapoints:
		maxprob_l = 0.0
		maxprob_r = 1.0
		for i in range(iters):
			maxprob_m = (maxprob_l + maxprob_r) / 2
			assignment = algorithms.PLRA(instance, maxprob = maxprob_m)
			relative_quality = metrics.quality(instance, assignment, relative = True)
			if (relative_quality >= datapoint - eps):
				maxprob_r = maxprob_m
			else:
				maxprob_l = maxprob_m
		ret[0].append(maxprob_r)
		ret[1].append(algorithms.PLRA(instance, maxprob = maxprob_r))
	return ret

def RunPMQ(instance, datapoints, maxprobs, offset, iters = 10, eps = 1e-4, mode = 0):
	# This function runs PM-Q and returns the assigments.
	# For the hyperparameter tuning, it relaxes Q to maxprob + offset and does binary
	# search to find the largest beta that satisfies the relative quality requirement.
	# Inputs arguments:
	# 	instance:   the input instance
	# 	datapoints: relative quality requirements
	#   maxprobs:   PLRA's maxprobs as a reference
	#   offset:     relaxation offset
	#   iters:      number of iterations in the binary search
	#   eps:        precision parameter
	#   mode:       return assignment or parameter
	# Output: A list of assignments for each relative quality requirement
	import metrics
	import algorithms
	ret = []
	for i in range(len(datapoints)):
		datapoint = datapoints[i]
		maxprob = min(maxprobs[i] + offset, 1.0)
		beta_l = 0.0
		beta_r = 1.0
		for i in range(iters):
			beta_m = (beta_l + beta_r) / 2
			assignment = algorithms.PMQ(instance, beta = beta_m, maxprob = maxprob)
			relative_quality = metrics.quality(instance, assignment, relative = True)
			if (relative_quality >= datapoint - eps):
				beta_l = beta_m
			else:
				beta_r = beta_m
		if (mode == 0):
			ret.append(algorithms.PMQ(instance, beta = beta_l, maxprob = maxprob))
		else:
			ret.append(beta_l)
	return ret

def RunPME(instance, datapoints, maxprobs, offset, iters = 10, eps = 1e-4, mode = 0):
	# This function runs PM-E and returns the assigments.
	# For the hyperparameter tuning, it relaxes Q to maxprob + offset and does binary
	# search to find the largest alpha that satisfies the relative quality requirement.
	# Inputs arguments:
	# 	instance:   the input instance
	# 	datapoints: relative quality requirements
	#   maxprobs:   PLRA's maxprobs as a reference
	#   offset:     relaxation offset
	#   iters:      number of iterations in the binary search
	#   eps:        precision parameter
	#   mode:       return assignment or parameter
	# Output: A list of assignments for each relative quality requirement
	import metrics
	import algorithms
	ret = []
	for i in range(len(datapoints)):
		datapoint = datapoints[i]
		maxprob = min(maxprobs[i] + offset, 1.0)
		alpha_l = 0.0
		alpha_r = 10.0
		for i in range(iters):
			alpha_m = (alpha_l + alpha_r) / 2
			assignment = algorithms.PME(instance, alpha = alpha_m, maxprob = maxprob)
			relative_quality = metrics.quality(instance, assignment, relative = True)
			if (relative_quality >= datapoint - eps):
				alpha_l = alpha_m
			else:
				alpha_r = alpha_m
		if (mode == 0):
			ret.append(algorithms.PME(instance, alpha = alpha_l, maxprob = maxprob))
		else:
			ret.append(alpha_l)
	return ret