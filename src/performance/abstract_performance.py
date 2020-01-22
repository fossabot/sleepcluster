'''
Performance Metric

Analysis of the state model:
	# Clusters >= 3 (For lab: 4)
	% Ordered unambiguity (1 class, 2 class, etc)

Analysis of the classifications:
	1-1 accuracy with labels
	Context tolerance

Context:
	Truth - Result - Tolerances
	R - AW:
		If up to 2 epochs before it is AW or QW and is continued by either AW or QW
		OR
		If up to 2 epochs after it is AW or QW
	R - QW:
		If up to 2 epochs before it is AW or QW and is continued by either AW or QW
		OR
		If up to 2 epochs after it is AW or QW
	R - NR:
		If up to 2 epochs before it is NR and is continued by either NR or R
	NR - AW:


Target consensus:
	Priority - Take the highest priority for conflicting epochs
	Context - Take the label that makes the most sense in Context
	Combined - Take the best weighted Priority + Context
'''
# Given a mapping, labels, and targets:
#	Calculate the performance of the labelling
#	 - Specific to the state model (e.g. 4-state model)

import numpy as np
from abc import ABC, abstractmethod

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
