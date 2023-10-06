# Parse the arguments
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("dataset", help = "name of the dataset")
parser.add_argument("offset", help = "offset in maximum probability", type = float)
args = parser.parse_args()

# Set up the dataset being tested and the relative quality requirements
dataset = args.dataset
offset  = args.offset
datapoints = [0.8, 0.85, 0.9, 0.95, 0.98, 0.99, 0.995, 1.0]

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
[maxprobs, ret[0]] = utils.RunPLRA(instance, datapoints)
ret[1] = utils.RunPMQ(instance, datapoints, maxprobs, offset)
ret[2] = utils.RunPME(instance, datapoints, maxprobs, offset)

# Save up the results in a .log file
file = open('logs/' + dataset.lower() + '_main.log', 'w')
for i in range(num_algorithms):
	quality = []
	metrici = [[] for j in range(5)]
	for assigment in ret[i]:
		quality.append(metrics.quality(instance, assigment, relative = True))
		for j in range(5):
			metrici[j].append(metrics.calc(instance, assigment, j)) 
	file.write(str(quality))
	file.write('\n')
	file.write(str(metrici))
	file.write('\n')
file.close()