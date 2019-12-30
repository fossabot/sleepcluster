from abc import ABC, abstractmethod
import os
import numpy as np
from xlwt import Workbook

# Processor defines the Class structure and necessary components
#	to a Data Processor plugin
class Processor(ABC):

	def __init__(self):
		pass
		
	def __str__(self):
		return type(self).__name__
		
	@abstractmethod
	def process(self, *args, **kwargs):
		raise NotImplementedError( "No process function implemented" )	
		
	def write(self, name, header, data, location):
		if header.shape[1] != header.shape[1]:
			raise ValueError("Dimensions of header and data do not match")
		if os.path.isfile(location):
			os.remove(location)
		wb = Workbook()
		ws = wb.add_sheet(name)
		for row in range(header.shape[0]):
			for col in range(header.shape[1]):
				ws.write(row, col, header[row][col])
		for row in range(1, 1 + data.shape[0]):
			for col in range(data.shape[1]):
				ws.write(row, col, data[row][col])
		wb.save(location)