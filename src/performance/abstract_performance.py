import numpy as np
from abc import ABC, abstractmethod

from maps import map

# Performance defines the Class structure and necessary components
#	to a Performance Calculator plugin
class Performance(ABC):

	def __init__(self, classes=3):
		self.classes = classes

	def __str__(self):
		return type(self).__name__ + " with " + str(self.classes) + " classes"

	@abstractmethod
	def calculateAccuracy(self, mapping, labels, targets):
		raise NotImplementedError("No calculateAccuracy function implemented")

	def bestMapping(self, maps, labels, targets):
		best_accuracy = -1
		best_map = None
		for mapping in maps:
			translation = map.Map.translate(mapping, labels)
			accuracy = self.calculateAccuracy(translation, targets)
			if accuracy > best_accuracy:
				best_accuracy = accuracy
				best_map = mappinig
		return best_map, best_accuracy
