import numpy as np
from abc import ABC, abstractmethod

# Cluster defines the Class structure and necessary components
#	to a Cluster Algorithm plugin
class Cluster(ABC):

	@classmethod
	def __init__(self, type=None):
		self.type = None
		
	def __str__(self):
		return type(self).__name__ + ": " + self.type

	