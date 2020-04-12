"""smrMAT Reader"""

# Authors: Jeffrey Wang
# License: BSD 3 clause

import numpy as np
from scipy.io import loadmat

from ..utils import DataObject
from . import BaseReader

# A Data Importer for .mat files exported by Spike2 v7
class smrMATreader(BaseReader):
	standard = ".mat files exported by Spike2 v7"
	filetypes = [("MAT-files", "*.mat")]

	def __init__(self, filepath):
		super().__init__(filepath)

	def read(self, c="", score=False, map={}):
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
				channel = matfile[field][0][0][0][0]
				channels.append(channel)
				if score and c == channel:
					data, dataObject = self.score_read(matfile[field][0][0], map)
				elif c == channel:
					data, dataObject = self.data_read(matfile[field][0][0])
		if data.size == 0:
			raise FileNotFoundError("Channel named " + c + " not found. Instead found: " + str(channels))
		return dataObject

	def score_read(channel, map):
		try:
			data = channel[7].flatten()[:-1]
			for k, v in map.items():
				data[data == k] = v
			data = data.astype(int)
			resolution = channel[2][0][0]
			length = int(channel[3][0][0])
			dataObject = DataObject(name=c, data=data, resolution=resolution, length=length)
		except Exception:
			raise FileNotFoundError("An error occurred extracting from channel " + c)
		return data, dataObject

	def data_read(channel):
		try:
			data = channel[8].flatten()
			resolution = channel[2][0][0]
			length = int(channel[7][0][0])
			dataObject = DataObject(name=c, data=data, resolution=resolution, length=length)
		except Exception:
			raise FileNotFoundError("An error occurred extracting from channel " + c)
		return data, dataObject
