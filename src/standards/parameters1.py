from standards import abstract_standards as standards
from abc import ABC, abstractmethod


# Parameters1 defines the necessary parameters
#	to a SleepCluster Standard of the Parameters1 standard
class Parameters1(standards.Standards):
	
	def __init__(self):
		self.NORMALIZER = None
		self.EPOCH_SIZE = -1
		self.PERCENTILE = -1
		self.BANDS = []
	