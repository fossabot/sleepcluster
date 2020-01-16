

class Dataset:
	
	def __init__(self, locations, features, length):
		self.locations = locations
		self.features = features
		self.length = length
		self.num_features = len(features)
		
	def __str__(self):
		return type(self).__name__
		

def writeDataset(dataset, location):
	with open(location, 'w') as file:
		file.write(str(len(dataset.locations)) + '\n')
		file.write(str(dataset.num_features) + '\n')
		file.write(str(dataset.length) + '\n')
		string = ""
		for feature in dataset.features:
			string += feature + ","
		file.write(string[:-1] + '\n')
		for item in dataset.locations:
			file.write(item + "\n")
	
def readDataset(location):
	with open(location, 'r') as file:
		num_datasets = int(file.readline())
		num_features = int(file.readline())
		length = int(file.readline())
		features = file.readline().split(',')
		locations = []
		for i in range(num_datasets):
			locations.append(file.readline())
	return Dataset(locations, features, length)
	
def mergeDatasets(datasets):
	compare = datasets[0]
	length = 0
	locations = []
	for ds in datasets:
		if compare.features != ds.features:
			raise ValueError("Datasets contain different sets or orderings of features")
		else:
			length += ds.length
			locations.append(ds.locations)
	return Dataset(locations, compare.features, length)