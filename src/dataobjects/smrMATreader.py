import numpy as np
from scipy.io import loadmat

from dataobjects import dataobject
from dataobjects import abstract_datareader as dataReader

# A Data Importer (DataReader) plugin for .mat files exported by Spike2 v7
class smrMATreader(dataReader.DataReader):
	standard = ".mat files exported by Spike2 v7"
	filetypes = [("MAT-files", "*.mat")]

	def __init__(self, filepath):
		super().__init__(filepath)

	# Read data out from specified channel in file and return a DataObject storing that data
	def read(self, c="", score=False, map=None):
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
				if score and c == matfile[field][0][0][0][0]:
					try:
						data = matfile[field][0][0][7].flatten()[:-1]
						for k, v in map.items():
							data[data == k] = v
						data = data.astype(int)
						resolution = matfile[field][0][0][2][0][0]
						length = int(matfile[field][0][0][3][0][0])
						dataObject = dataobject.DataObject(name=c, data=data, resolution=resolution, length=length)
					except Exception:
						raise FileNotFoundError("An error occurred extracting from channel " + c)
				elif c == matfile[field][0][0][0][0]:
						try:
							data = matfile[field][0][0][8].flatten()
							resolution = matfile[field][0][0][2][0][0]
							length = int(matfile[field][0][0][7][0][0])
							dataObject = dataobject.DataObject(name=c, data=data, resolution=resolution, length=length)
						except Exception:
							raise FileNotFoundError("An error occurred extracting from channel " + c)
		if data.size == 0:
			raise FileNotFoundError("Channel named " + c + " not found. Instead found: " + str(channels))
		return dataObject
