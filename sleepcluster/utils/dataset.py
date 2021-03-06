"""Dataset"""

# Authors: Jeffrey Wang
# License: BSD 3 clause

import numpy as np
from xlrd import open_workbook


# Dataset is a collection of processed .xls files that contain feature data
class Dataset:

	def __init__(self, files, features):
		self.files = files
		self.features = features
		self.total_length = np.sum([file['length'] for file in self.files if 'length' in file])
		self.num_files = len(files)
		self.num_features = len(features)

	def __str__(self):
		return type(self).__name__

	def load(self, index):
		np_headers = np.array([self.features])
		data = []
		file = self.files[index]
		book = open_workbook(file['location'])
		sheet = book.sheet_by_index(0)
		length = file['length']
		for row in range(length):
			data.append(sheet.row_slice(rowx=row,start_colx=0, end_colx=self.num_features))
		np_data = np.array(data)
		return {'headers': np_headers, 'data': np_data}

	def write(self, location):
		with open(location, 'w') as file:
			file.write(str(len(self.files)) + '\n')
			file.write(str(self.num_features) + '\n')
			string = ""
			lengths = [file['length'] for file in self.files if 'length' in file]
			for length in lengths:
				string += str(length) + ","
			file.write(string[:-1] + '\n')
			file.write(str(self.total_length) + '\n')
			string = ""
			for feature in self.features:
				string += feature + ","
			file.write(string[:-1] + '\n')
			locations = [file['location'] for file in self.files if 'location' in file]
			for item in locations:
				file.write(item + "\n")

	@staticmethod
	def readDataset(location):
		with open(location, 'r') as file:
			num_datasets = int(file.readline())
			num_features = int(file.readline())
			lengths = file.readline().split(',')
			for i in range(len(lengths)):
				lengths[i] = int(lengths[i])
			features = file.readline().split(',')
			locations = []
			for i in range(num_datasets):
				locations.append(file.readline())
			files = []
			for length, loc in zip(lengths, locations):
				files.append({'location': loc, 'length': length})
		return Dataset(files, features)

	@staticmethod
	def mergeDatasets(datasets):
		compare = datasets[0]
		files = []
		lengths = []
		locations = []
		for ds in datasets:
			if compare.features != ds.features:
				raise ValueError("Datasets contain different sets or orderings of features")
			else:
				files.append(ds.files)
		return Dataset(files, compare.features)
