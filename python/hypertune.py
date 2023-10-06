# Parse the arguments
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("dataset", help = "name of the dataset")
parser.add_argument("maxprob", help = "maximum probability at 95% quality", type = float)
parser.add_argument("steplength", help = "step length", type = float)
args = parser.parse_args()

# Set up the dataset being tested and the relative quality requirements
dataset = args.dataset
maxprob = args.maxprob
steplength = args.steplength
datapoint = 0.95

# Import the relavant codes
import utils
import classes
import metrics

# Read the dataset and calculate the maximum possible quality
instance = classes.InputInstance(dataset)

# Run the algorithms
num_algorithms = 3
algorithms = ['PLRA', 'PM-Q', 'PM-E']
ret = [[] for i in range(num_algorithms)]
[_, ret[0]] = utils.RunPLRA(instance, [datapoint])
for i in range(6):
	ret[1] += utils.RunPMQ(instance, [datapoint], [maxprob], steplength * i)
	ret[2] += utils.RunPME(instance, [datapoint], [maxprob], steplength * i)

# Save up the results in a .log file
file = open('logs/' + dataset.lower() + '_hypertune.log', 'w')
for i in range(num_algorithms):
	metrici = [[] for j in range(5)]
	for assigment in ret[i]:
		for j in range(5):
			metrici[j].append(metrics.calc(instance, assigment, j)) 
	file.write(str(metrici))
	file.write('\n')
file.close()