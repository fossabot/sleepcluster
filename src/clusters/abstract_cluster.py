import numpy as np
from abc import ABC, abstractmethod

# Cluster defines the Class structure and necessary components
#	to a Cluster Algorithm plugin
class Cluster(ABC):

	def __init__(self):
		self.cluster = None

	def __str__(self):
		return type(self).__name__

	@abstractmethod
	def fit(self, *args, **kwargs):
		raise NotImplementedError( "No fit function implemented" )

	@abstractmethod
	def predict(self, *args, **kwargs):
		raise NotImplementedError( "No predict function implemented" )
