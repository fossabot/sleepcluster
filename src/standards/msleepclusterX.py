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
		self.NPERSEG_FACTOR = {}
		self.NOVERLAP_FACTOR = {}
		self.DETREND = {}
		self.validateParameters()
		
	def validateParameters():
		if not(isintance(self.EPOCH_SIZE, float) or isinstance(self.EPOCH_SIZE, int)) or \
			self.EPOCH_SIZE <= 0:
			raise standards.ParameterError("EPOCH_SIZE", "Must be a positive number")
		if not(isintance(self.PERCENTILE, float) or isinstance(self.PERCENTILE, int)) or \
			self.PERCENTILE < 0 or self.PERCENTILE > 1:
			raise standards.ParameterError("PERCENTILE", "Must be a number between 0 and 1, inclusive")
		for band in bands:
			if len(band) != 2:
				raise standards.ParameterError("BANDS", "Bands must be intervals")
			elif band[0] <= 0 or band[1] <= band[0]:
				raise standards.ParameterError("BANDS", "Bands must be valid positive interval ranges")
		if self.NPERSEG_FACTOR.keys() != self.NOVERLAP_FACTOR.keys() or self.NPERSEG_FACTOR.keys() != DETREND:
			raise standards.ParameterError("KEYERROR", "Keys in NPERSEG_FACTOR, NOVERLAP_FACTOR, and DETREND must be the same")
		for key in self.NPERSEG_FACTOR.keys():
			if not(isinstance(self.NPERSEG_FACTOR[key], float) or isinstance(self.NPERSEG_FACTOR[key], int)) or \
				self.NPERSEG_FACTOR[key] <= 0 or self.NPERSEG_FACTOR[key] > 1:
				raise standards.ParameterError("NPERSEG_FACTOR", "Must be a number greater than 0 and less than or equal to 1")
			if not(isinstance(self.NOVERLAP_FACTOR[key], float) or isinstance(self.NOVERLAP_FACTOR[key], int)) or \
				self.NOVERLAP_FACTOR[key] <= 0 or self.NOVERLAP_FACTOR[key] > 1:
				raise standards.ParameterError("NOVERLAP_FACTOR", "Must be a number greater than 0 and less than or equal to 1")
			if not(isinstance(self.DETREND[key], str)) or self.NOVERLAP_FACTOR[key] not in ['linear', 'constant']:
				raise standards.ParameterError("DETREND", "Must be either 'linear' or 'constant'")
			