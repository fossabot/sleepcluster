import numpy as np
from performance import abstract_performance as performance

# A Performance plugin that runs a 1-1 accuracy metric
class SimplePerformance(performance.Performance):

	def __init__(self, classes=3):
		self.classes = classes

	def __str__(self):
		return type(self).__name__ + " with " + str(self.classes) + " classes"

	def calculateAccuracy(self, mapping, labels, targets):
		correct = 0
		total = len(labels)
		for label, target in zip(labels, targets):
			if label == target:
				correct += 1
		return correct / total
