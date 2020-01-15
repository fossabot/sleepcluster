from abc import ABC, abstractmethod

# Exception defined by an invalid parameter
class ParameterError(Exception):
	def __init__(self, parameter, message):
		self.parameter = parameter
		self.message = message
		
# Standards defines the Class structure and necessary components
#	to a SleepCluster Standard
class Standards(ABC):
	
	def __init__(self):
		pass
		
	def __str__(self):
		return type(self).__name__
		
	@abstractmethod
	def validateParameters():
		raise NotImplementedError( "No validateParameters function implemented" )	