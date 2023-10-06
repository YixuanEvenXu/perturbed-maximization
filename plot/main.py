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
args = parser.parse_args()
file = open('logs/' + args.dataset.lower() + '_main.log', 'r')
lines = file.readlines()
file.close()

# Read the logs
num_algorithms = 3
algorithms = ['PLRA', 'PM-Q', 'PM-E']
quality = []
metrici = []
for i in range(num_algorithms):
	quality.append(eval(lines[2 * i]))
	metrici.append(eval(lines[2 * i + 1]))

# Plot the results and save as a jpg file
import matplotlib.pyplot as plt
for i in range(5):
	plt.figure(figsize=(9, 4.5))
	plt.subplots_adjust(top = 0.96, bottom = 0.21, right = 0.97, left = 0.20)
	plt.xlabel('Relative Quality', fontsize = 28) 
	plt.ylabel(metrics.name(i, style = 2), fontsize = 28)
	plt.xticks([0.8, 0.85, 0.9, 0.95, 1], fontsize = 28)
	plt.yticks(fontsize = 28)
	plt.plot(quality[0], metrici[0][i], marker = 's', markerfacecolor = 'none', markersize = 25, markeredgewidth = 5, alpha = 0.7, linewidth = 3)
	plt.plot(quality[1], metrici[1][i], marker = '+', markersize = 25, markeredgewidth = 5, alpha = 0.7, linewidth = 3)
	plt.plot(quality[2], metrici[2][i], marker = 'x', markersize = 25, markeredgewidth = 5, alpha = 0.7, linewidth = 3)
	if (i == 1 or i == 0 and args.dataset == 'AAMAS2015'):
		plt.legend(labels = algorithms, loc = 'best', fontsize = 28)
	plt.savefig('figures/' + args.dataset.lower() + '_main/' + metrics.name(i, style = 1) + '.pdf')
	plt.clf()