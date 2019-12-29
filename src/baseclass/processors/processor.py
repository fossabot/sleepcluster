from abc import ABC, abstractmethod

# Processor defines the Class structure and necessary components
#	to a Data Processor plugin
class Processor(ABC):

	def __init__(self):
		pass
		
	def __str__(self):
		return type(self).__name__
		
	@abstractmethod
	def process(self, data):
		raise NotImplementedError( "No process function implemented" )	