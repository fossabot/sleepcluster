import numpy as np
from abc import ABC, abstractmethod

# Cluster defines the Class structure and necessary components
#	to a Cluster Algorithm plugin
class Cluster(ABC):

	def __init__(self):
		pass
		
	def __str__(self):
		return type(self).__name__

	@abstractmethod
	def cluster(self, *args, **kwargs):
		raise NotImplementedError( "No cluster function implemented" )	