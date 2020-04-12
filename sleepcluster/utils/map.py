"""Map"""

# Authors: Jeffrey Wang
# License: BSD 3 clause

import numpy as np
import itertools

# Map is a plugin that determines all possible mapping permutations
#	between the given class size and the desired class size
class Map():

	def __init__(self, classes=3):
		self.classes = classes

	def __str__(self):
		return type(self).__name__ + " with " + str(self.classes) + " classes"

	def map(self, num_clusters):
		if num_clusters < self.classes:
			raise ValueError("Must input at least as many classes as desired")
		maps = []
		for permutation in list(itertools.permutations(np.arange(num_clusters))):
			mapping = {}
			for i in range(len(permutation)):
				mapping[permutation[i]] = i % self.classes
			maps.append(mapping)
		return maps

	@staticmethod
	def translate(mapping, labels):
		new_labels = []
		for label in labels:
			new_labels.append(mapping[label])
		return new_labels
