# Parse the arguments
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("dataset", help = "name of the dataset")
parser.add_argument("offset", help = "offset in maximum probability", type = float)
args = parser.parse_args()

# Set up the dataset being tested and the relative quality requirements
dataset = args.dataset
offset  = args.offset
datapoints = [0.95]

# Import the relavant codes
import utils
import classes
import metrics

# Read the dataset and calculate the maximum possible quality
instance = classes.InputInstance(dataset)

# Run the algorithms
[maxprobs, _] = utils.RunPLRA(instance, datapoints)
betas  = utils.RunPMQ(instance, datapoints, maxprobs, offset, mode = 1)
alphas = utils.RunPME(instance, datapoints, maxprobs, offset, mode = 1)

# Save up the results in a .log file
file = open('logs/' + dataset.lower() + '_parameter.log', 'w')
file.write(str(maxprobs))
file.write('\n')
file.write(str(betas))
file.write('\n')
file.write(str(alphas))
file.write('\n')
file.close()