from importlib.machinery import SourceFileLoader
dataReader = SourceFileLoader("abstract_datareader", "./dataobjects/abstract_datareader.py").load_module()

import numpy as np
from scipy.io import loadmat

import dataobjects.dataobject as dataobject

# A Data Importer (DataReader) plugin for .mat files exported by Spike2 v7
class smrMAT(dataReader.DataReader):
	standard = ".mat files exported by Spike2 v7"
	filetypes = [("MAT-files", "*.mat")]

	def __init__(self, filepath):
		super().__init__(filepath)
		
	# Read data out from specified channel in file and return a DataObject storing that data
	def read(self, c=""):
		if c == "":
			raise FileNotFoundError("Channel or score channel has not been specified")
		try:
			matfile = loadmat(self.filepath)
		except:
			raise FileNotFoundError("No such file or directory: " + self.filepath)
		channels = []
		data = np.zeros(0)
		for field in matfile.keys():
			if '_Ch' in field:
				channels.append(matfile[field][0][0][0][0])
			if c == matfile[field][0][0][0][0]:
				try:
					data = np.absolute((matfile[field][0][0][8]).flatten())
					resolution = matfile[field][0][0][2][0][0]
					length = matfile[field][0][0][7][0][0]
					dataObject = dataobject.DataObject(name=c, data=data, resolution=resolution, length=length)
				except Exception:
					raise FileNotFoundError("An error occurred extracting from channel " + c)
		if data.size == 0:
			raise FileNotFoundError("Channel named " + c + " not found. Instead found: " + str(channels))
		return dataObject