# Parse the arguments
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("dataset", help = "name of the dataset")
parser.add_argument("algorithm", help = "name of the algorithm")
parser.add_argument("maxprob", help = "Q", type = float)
parser.add_argument("beta", help = "β", type = float)
parser.add_argument("alpha", help = "α", type = float)
parser.add_argument("offset", help = "Increment in Q", type = float)
args = parser.parse_args()

# Set up the dataset being tested and the algorithm
dataset   = args.dataset
algorithm = args.algorithm
maxprob   = args.maxprob
beta      = args.beta
alpha     = args.alpha
offset    = args.offset

# Import the relavant codes
import algorithms
import classes
import metrics
import numpy as np

# Read the dataset and calculate the maximum possible quality
instance = classes.InputInstance(dataset, init = False)

# Run the algorithm
if (algorithm == 'PLRA'):
	assigment = algorithms.PLRA(instance, maxprob = maxprob)
elif (algorithm == 'PM-Q'):
	assigment = algorithms.PMQ(instance, beta = beta, maxprob = maxprob + offset)
elif (algorithm == 'PM-E'):
	assigment = algorithms.PME(instance, alpha = alpha, maxprob = maxprob + offset)
else:
	print("Algorithm name is incorrect.")

# Output statistics
pquality = 0
for i in range(instance.np):
	for j in range(instance.nr):
		if (algorithm == 'PM-Q'):
			pquality += (assigment[i][j] - assigment[i][j] * assigment[i][j] * beta) * instance.s[i][j]
		if (algorithm == 'PM-E'):
			pquality += (1 - np.exp(-alpha * assigment[i][j])) * instance.s[i][j]
print(f'Quality: {metrics.quality(instance, assigment):.2f}')
print(f'PQuality: {pquality:.2f}')
for i in range(5):
	print(f'{metrics.name(i, style = 2)}: {metrics.calc(instance, assigment, i):.2f}')