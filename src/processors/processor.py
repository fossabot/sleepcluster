import numpy as np
from abc import ABC, abstractmethod

# Processor defines the Class structure and necessary components
#	to a Data Processor plugin
class Processor(ABC):

	@classmethod
	def __init__(self, type=None):
		self.type = None
		
	def __str__(self):
		return type(self).__name__ + ": " + self.type

	