# Set up the dataset being tested and the relative quality requirements
dataset = 'counter'

# Import the relavant algorithms
import algorithms
import classes
import metrics

# Read the dataset and calculate the maximum possible quality
instance = classes.InputInstance(dataset)

# Test the algorithms
best = metrics.quality(instance, algorithms.PLRA(instance))
x = []
y = []
for i in range(50):
	alpha = i / 2.5
	x.append(alpha)
	y.append(metrics.quality(instance, algorithms.PME(instance, alpha = alpha), relative = True))

# Plot the results
import matplotlib.pyplot as plt
plt.plot(x, y, linewidth = 3)
plt.xticks(fontsize = 18)
plt.yticks(fontsize = 18)
plt.xlabel('Alpha', fontsize = 18)
plt.ylabel('Relative Quality', fontsize = 18)
plt.subplots_adjust(top = 0.98, bottom = 0.15, right = 0.97, left = 0.19)
plt.savefig('figures/counter_example.pdf')
plt.clf()