from standards import abstract_sleepcluster as standards
from abc import ABC, abstractmethod


# mSleepClusterX defines the necessary parameters
#	to a SleepCluster Standard of the mSleepClusterX type
class mSleepClusterX(standards.Standards):
	
	def __init__(self):
		self.NORMALIZER = None
		self.parameters.NORMALIZE_ARG = None
		self.EPOCH_SIZE = -1
		self.PERCENTILE = -1
		self.BANDS = []
		self.NPERSEG_FACTOR = 1
		self.NOVERLAP_FACTOR = 0.5
		self.DETREND = 'linear'
		self.validateParameters()
		
	def validateParameters():
		if not(isintance(self.EPOCH_SIZE, float) or isinstance(self.EPOCH_SIZE, int)) or \
			self.EPOCH_SIZE <= 0:
			raise standards.ParameterError("EPOCH_SIZE", "Must be a positive number")
		if not(isintance(self.PERCENTILE, float) or isinstance(self.PERCENTILE, int)) or \
			self.PERCENTILE < 0 or self.PERCENTILE > 1:
			raise standards.ParameterError("PERCENTILE", "Must be a number between 0 and 1, inclusive")
		if not(isintance(self.NPERSEG_FACTOR, float) or isinstance(self.NPERSEG_FACTOR, int)) or \
			self.NPERSEG_FACTOR <= 0:
			raise standards.ParameterError("EPOCH_SIZE", "Must be a positive number")
		if not(isintance(self.NOVERLAP_FACTOR, float) or isinstance(self.NOVERLAP_FACTOR, int)) or \
			self.NOVERLAP_FACTOR <= 0:
			raise standards.ParameterError("EPOCH_SIZE", "Must be a positive number")