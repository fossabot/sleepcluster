

class Dataset:
	
	def __init__(self, locations, features, length):
		self.locations = locations
		self.features = features
		self.length = length
		self.num_features = len(features)
		
	def __str__(self):
		return type(self).__name__
		
	def writeDatasets(self, dataset, location):
		with open(location, 'w') as file:
			file.write(dataset['headers']['num_datasets'] + '\n')
			file.write(dataset['headers']['num_features'] + '\n')
			file.write(dataset['headers']['length'] + '\n')
			string = ""
			for i in range(len(dataset['headers']['features'])):
				string += dataset['headers']['features'] + ","
			file.write(string[:-1] + '\n')
			for item in dataset['location']:
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
		data_dict = {}
		data_dict['location'] = locations
		data_dict['headers'] = {
								'num_datasets': len(datasets),
								'num_features': compare.num_features,
								'features': compare.features,
								'total_length': length
		return data_dict