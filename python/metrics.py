# This file defines different metrics about the randomized assignment

def quality(instance, assignment, relative = False):
	# Matching quality calculator
	# Inputs arguments:
	# 	instance:   the input instance
	# 	assignment: the assignment matrix
	#   relative:   whether to calculate the relative quality
	# Output: the (relative) quality of the matching
	ret = 0
	for i in range(instance.np):
		for j in range(instance.nr):
			ret += instance.s[i][j] * assignment[i][j]
	if (relative):
		return ret / instance.max_quality
	else:
		return ret

def maxprob(instance, assignment):
	# Matching maxprob calculator
	# Inputs arguments:
	# 	instance:   the input instance
	# 	assignment: the assignment matrix
	# Output: the maximum assignment probability of the matching
	ret = 0.0
	for i in range(instance.np):
		ret = max(ret, max(assignment[i]))
	return ret

def avgmaxprob(instance, assignment):
	# Matching avgmaxprob calculator
	# Inputs arguments:
	# 	instance:   the input instance
	# 	assignment: the assignment matrix
	# Output: the average maximum assignment probability of each paper
	ret = 0
	for i in range(instance.np):
		ret += max(assignment[i])
	ret /= instance.np
	return ret

def supportsize(instance, assignment):
	# Matching support size calculator
	# Inputs arguments:
	# 	instance:   the input instance
	# 	assignment: the assignment matrix
	# Output: the support size of the assignment matrix
	ret = 0
	for i in range(instance.np):
		for j in range(instance.nr):
			ret += (assignment[i][j] >= 1e-6)
	return ret

def entropy(instance, assignment):
	# Matching entropy calculator
	# Inputs arguments:
	# 	instance:   the input instance
	# 	assignment: the assignment matrix
	# Output: the entropy of the matching
	from numpy import log
	ret = 0
	for i in range(instance.np):
		for j in range(instance.nr):
			if (assignment[i][j] > 0):
				ret -= assignment[i][j] * log(assignment[i][j])
	return ret

def l2normloss(instance, assignment):
	# Matching l2normloss calculator
	# Inputs arguments:
	# 	instance:   the input instance
	# 	assignment: the assignment matrix
	# Output: the Frobenius norm of the assignment matrix
	from numpy import sqrt
	ret = 0
	for i in range(instance.np):
		for j in range(instance.nr):
			ret += assignment[i][j] * assignment[i][j]
	ret = sqrt(ret)
	return ret

def name(num, style = 0):
	# Return names of the metrics
	# Inputs arguments:
	# 	num:   the metric number 
	#   style: the style of the name
	# Output: the corresponding name
	if (style == 0):
		if (num == 0):
			return 'Maximum Probability'
		if (num == 1):
			return 'Average Maximum Probability'
		if (num == 2):
			return 'Support Size'
		if (num == 3):
			return 'Entropy'
		if (num == 4):
			return 'L2 Norm'
		return 'Metric Not Found'
	elif (style == 1):
		if (num == 0):
			return 'maximum_probability'
		if (num == 1):
			return 'average_maximum_probability'
		if (num == 2):
			return 'support_size'
		if (num == 3):
			return 'entropy'
		if (num == 4):
			return 'l2_norm'
		return 'metric_not_found'
	else:
		if (num == 0):
			return 'Maxprob'
		if (num == 1):
			return 'AvgMax'
		if (num == 2):
			return 'Support'
		if (num == 3):
			return 'Entropy'
		if (num == 4):
			return 'L2 Norm'
		return 'Error'

def calc(instance, assignment, num):
	# Calculate a specific metric according to metric number.
	# Inputs arguments:
	# 	instance:   the input instance
	# 	assignment: the assignment matrix
	#   num:        the metric number 
	# Output: the corresponding value
	if (num == 0):
		return maxprob(instance, assignment)
	if (num == 1):
		return avgmaxprob(instance, assignment)
	if (num == 2):
		return supportsize(instance, assignment)
	if (num == 3):
		return entropy(instance, assignment)
	if (num == 4):
		return l2normloss(instance, assignment)
	return 'Metric not found'