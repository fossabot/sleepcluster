"""Simple Analyzer"""

# Authors: Jeffrey Wang
# License: BSD 3 clause

import numpy as np
from . import BaseAnalyzer

# An Analyzer that runs a 1-1 accuracy metric
class SimpleAnalyzer(BaseAnalyzer):

	def __init__(self, classes=3):
		self.classes = classes

	def __str__(self):
		return type(self).__name__ + " with " + str(self.classes) + " classes"

	def calculate_accuracy(self, labels, targets):
		correct = 0
		total = len(labels)
		for label, target in zip(labels, targets):
			if label == target:
				correct += 1
		return correct / total
