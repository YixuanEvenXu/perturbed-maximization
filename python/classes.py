class InputInstance:
	# Input instance of randomized assignment algorithms
	# Members:
	# 	np:   number of papers
	#   nr:   number of reviewers
	# 	ellp: number of reviewers required per paper
	#   ellr: maximum number of papers per reviewer
	#   s:    similarity matrix, index: [paper][reviewer]
	#   max_quality: maximum possible quality
	def __init__(self, dataset, init = True):
		file = open('datasets/' + dataset.lower() + '.in', 'r')
		lines = file.readlines()
		file.close()
		# Read the number of papers and reviewers
		[self.np, self.nr] = list(map(int, lines[0].split(' ')))
		lines = lines[1 : ]
		# Read the similarity matrix
		self.s = []
		for line in lines:
			splitline = line.split(' ')
			while splitline[-1] == '\n':
				splitline.pop()
			self.s.append(list(map(float, splitline)))
		# Load the papers' requirement and reviewers' load limit
		self.ellp = 3
		self.ellr = 6 + 6 * (dataset[: 5] == 'AAMAS') + (dataset == 'Preflib2')
		if (dataset == 'counter'):
			self.ellp = 1
			self.ellr = 1
		# Initialize maximum quality
		if (init):
			import algorithms
			import metrics
			self.max_quality = metrics.quality(self, algorithms.PLRA(self, maxprob = 1))