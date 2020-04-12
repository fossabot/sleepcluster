"""Base Analyzer"""

# Authors: Jeffrey Wang
# License: BSD 3 clause

import numpy as np
from abc import ABC, abstractmethod

from ..utils import Map

# Performance defines the Class structure and necessary components
#	to an Analyzer
class BaseAnalyzer(ABC):

	def __init__(self, classes=3):
		self.classes = classes

	def __str__(self):
		return type(self).__name__ + " with " + str(self.classes) + " classes"

	@abstractmethod
	def calculate_accuracy(self, mapping, labels, targets):
		raise NotImplementedError("No calculateAccuracy function implemented")

	def bestMapping(self, maps, labels, targets):
		best_accuracy = -1
		best_map = None
		for mapping in maps:
			translation = Map.translate(mapping, labels)
			accuracy = self.calculate_accuracy(translation, targets)
			if accuracy > best_accuracy:
				best_accuracy = accuracy
				best_map = mapping
		return best_map, best_accuracy
