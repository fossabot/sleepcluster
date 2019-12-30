import numpy as np

# DataObject stores the data read in from a Data Importer
class DataObject():

	def __init__(self, name="", data=np.zeros(0), resolution=-1, length=-1):
		self.name = name
		self.data = data
		self.indices = np.arange(len(data))
		self.resolution = resolution
		self.length = length
		
	def __str__(self):
		return type(self).__name__ + ": " + self.name
						
	def get(self, arr, i, k=None):
		if len(arr) == 0:
			return False
		if isinstance(k, int):
			return arr[i:k]
		else:
			return arr[i]

	def getData(self, i, k=None):
		return self.get(self.data, i, k)

	def getIndices(self, i, k=None):
		return self.get(self.indices, i, k)
		
	def process(self, function):
		data = function(self.data)
		return DataObject(name=self.name, data=data, resolution=self.resolution, length=self.length)