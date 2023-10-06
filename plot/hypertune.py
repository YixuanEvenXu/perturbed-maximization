# Fix import path
import os
import sys
from pathlib import Path
sys.path.append(os.path.join(str(Path(__file__).resolve().parent.parent), 'python'))
import metrics

# Parse the arguments
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("dataset", help = "name of the dataset")
parser.add_argument("steplength", help = "step length", type = float)
args = parser.parse_args()
steplength = args.steplength
file = open('logs/' + args.dataset.lower() + '_hypertune.log', 'r')
lines = file.readlines()
file.close()

# Read the logs
num_algorithms = 3
legends = ['PLRA', 'PM-Q', 'PM-E', 'PM-Q Elbow', 'PM-E Elbow']
metrici = []
for i in range(num_algorithms):
	metrici.append(eval(lines[i]))
deltas = []
for i in range(6):
	deltas.append(i * steplength)

# Plot the results and save as a jpg file
import matplotlib.pyplot as plt
for i in range(5):
	plt.figure(figsize=(10, 5))
	plt.subplots_adjust(top = 0.96, bottom = 0.21, right = 0.97, left = 0.20)
	plt.xlabel('Delta', fontsize = 28) 
	plt.ylabel(metrics.name(i, style = 2), fontsize = 28)
	plt.xticks(deltas, fontsize = 28)
	plt.yticks(fontsize = 28)

	plt.plot([0], metrici[0][i], marker = 's', markerfacecolor = 'none', markersize = 15, markeredgewidth = 2, alpha = 0.7)
	plt.plot(deltas, metrici[1][i], marker = '+', markersize = 25, markeredgewidth = 5, alpha = 0.7, linewidth = 3)
	plt.plot(deltas, metrici[2][i], marker = 'x', markersize = 25, markeredgewidth = 5, alpha = 0.7, linewidth = 3)
	
	maxv = 0
	maxp = -1
	for j in range(6):
		value = abs(metrici[1][i][j] - metrici[0][i][0]) / abs(metrici[1][i][5] - metrici[0][i][0]) - j / 5
		if (value > maxv):
			maxv = value
			maxp = j
	plt.scatter(maxp * steplength, metrici[1][i][maxp], marker = '+', s = 450, linewidths = 8, alpha = 0.7, color = 'darkorange')
	
	maxv = 0
	maxp = -1
	for j in range(6):
		value = abs(metrici[2][i][j] - metrici[0][i][0]) / abs(metrici[2][i][5] - metrici[0][i][0]) - j / 5
		if (value > maxv):
			maxv = value
			maxp = j
	plt.scatter(maxp * steplength, metrici[2][i][maxp], marker = 'x', s = 450, linewidths = 8, alpha = 0.7, color = 'darkgreen')

	if (i == 4):
		plt.legend(labels = legends, loc = 'best', fontsize = 28)
	plt.savefig('figures/' + args.dataset.lower() + '_hypertune/' + metrics.name(i, style = 1) + '.pdf')
	plt.clf()