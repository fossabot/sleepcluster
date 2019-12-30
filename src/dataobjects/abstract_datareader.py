from abc import ABC, abstractmethod

# DataReader defines the Class structure and necessary components
#	to a Data Importer plugin
class DataReader(ABC):
	standard = "unspecified files"
	filetypes = []

	def __init__(self, filepath):
		self.filepath = filepath
		
	def __str__(self):
		return type(self).__name__ + " at " + self.filepath
		
	@abstractmethod
	def read(self, *args, **kwargs):
		raise NotImplementedError( "No read function implemented" )	