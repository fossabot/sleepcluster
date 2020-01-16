from standards import abstract_sleepcluster as standards
from abc import ABC, abstractmethod


# mSleepClusterX defines the necessary parameters
#	to a SleepCluster Standard of the mSleepClusterX type
class mSleepClusterX(standards.Standards):
	
	def __init__(self):
		self.CHANNELS = {
							'EEG':-1,
							'EMG':-1
						}
		self.EPOCH_SIZE = -1
		
		self.NORMALIZER = 		{	'EEG': None, 	'EMG': None	}
		self.NORMALIZE_ARG = 	{ 	'EEG': None, 	'EMG': None	}
		
		self.NPERSEG_FACTOR = 	{ 	'EEG': -1,		'EMG': -1	}
		self.NOVERLAP_FACTOR = 	{ 	'EEG': -1, 		'EMG': -1 	}
		self.DETREND = 			{ 	'EEG': None, 	'EMG': None 	}
		
		self.MERGERS = ['MAX','MEAN']
		self.FEATURES = {
							'0.BANDS':			{
													'EEG': None,
													'EMG': None,
													'merge': None
												},
							'1.ENTROPY': 		{ 	'EEG': False,	'EMG': False, 	'merge': None 	},
							'2.RMS': 			{ 	'EEG': False,	'EMG': False, 	'merge': None 	},
							'3.PERCENTILE': 	{ 	'EEG': None, 	'EMG': None, 	'merge': None	},
							'4.MEAN':			{ 	'EEG': False, 	'EMG': False, 	'merge': None	}
						}
		self.validateParameters()
		
	def validateParameters():
		for key in self.CHANNELS.keys():
			if not(isinstance(self.CHANNELS[key], float) or isinstance(self.CHANNELS[key], int)) or \
				self.CHANNELS[key] < 0:
				raise standards.ParameterError("CHANNELS", "Must have non-negative number of channels")
		if not(isintance(self.EPOCH_SIZE, float) or isinstance(self.EPOCH_SIZE, int)) or \
			self.EPOCH_SIZE <= 0:
			raise standards.ParameterError("EPOCH_SIZE", "Must be a positive number")
		for feature in self.FEATURES.keys():
			if self.CHANNELS.keys() != self.FEATURES[feature].keys():
				raise standards.ParameterError("KEYERROR", "Keys in " + feature + " must match CHANNELS")
			for key in self.CHANNELS.keys():
				if "BANDs" in feature:
					for band in self.FEATURES[feature][key]:
						if len(band) != 2:
							raise standards.ParameterError("BANDS", "Must be intervals")
						elif band[0] <= 0 or band[1] <= band[0]:
							raise standards.ParameterError("BANDS", "Must be valid positive interval ranges")
					if self.FEATURES[feature]['merge'] not in self.MERGERS:
						raise standards.ParameterError("BANDS", "Merger must be one of " + self.MERGERS)
				elif "ENTROPY" in feature:
					if self.FEATURES[feature][key] not in [True, False]:
						raise standards.ParameterError("ENTROPY", "Must be toggled to True or False")
					if self.FEATURES[feature]['merge'] not in self.MERGERS:
						raise standards.ParameterError("ENTROPY", "Merger must be one of " + self.MERGERS)
				elif "RMS" in feature:
					if self.FEATURES[feature][key] not in [True, False]:
						raise standards.ParameterError("RMS", "Must be toggled to True or False")
					if self.FEATURES[feature]['merge'] not in self.MERGERS:
						raise standards.ParameterError("RMS", "Merger must be one of " + self.MERGERS)
				elif "PERCENTILE" in feature:
					if not(isintance(self.FEATURES[feature][key], float) or \
							isinstance(self.FEATURES[feature][key], int) or \
							self.FEATURES[feature][key] is None) or \
							self.FEATURES[feature][key] < 0 or self.FEATURES[feature][key] > 1:
						raise standards.ParameterError("PERCENTILE", "Must be a number between 0 and 1, inclusive")
					if self.FEATURES[feature]['merge'] not in self.MERGERS:
						raise standards.ParameterError("PERCENTILE", "Merger must be one of " + self.MERGERS)
				elif "MEAN" in feature:
					if self.FEATURES[feature][key] not in [True, False]:
						raise standards.ParameterError("MEAN", "Must be toggled to True or False")
					if self.FEATURES[feature]['merge'] not in self.MERGERS:
						raise standards.ParameterError("MEAN", "Merger must be one of " + self.MERGERS)				
		if self.CHANNELS.keys() != self.NPERSEG_FACTOR.keys():
			raise standards.ParameterError("KEYERROR", "Keys in NPERSEG_FACTOR must match CHANNELS")
		if self.CHANNELS.keys() != self.NOVERLAP_FACTOR.keys():
			raise standards.ParameterError("KEYERROR", "Keys in NOVERLAP_FACTOR must match CHANNELS")
		if self.CHANNELS.keys() != self.DETREND.keys():
			raise standards.ParameterError("KEYERROR", "Keys in DETREND must match CHANNELS")
		for key in self.CHANNELS.keys():
			if not(isinstance(self.NPERSEG_FACTOR[key], float) or isinstance(self.NPERSEG_FACTOR[key], int)) or \
				self.NPERSEG_FACTOR[key] <= 0 or self.NPERSEG_FACTOR[key] > 1:
				raise standards.ParameterError("NPERSEG_FACTOR", "Must be a number greater than 0 and less than or equal to 1")
			if not(isinstance(self.NOVERLAP_FACTOR[key], float) or isinstance(self.NOVERLAP_FACTOR[key], int)) or \
				self.NOVERLAP_FACTOR[key] <= 0 or self.NOVERLAP_FACTOR[key] > 1:
				raise standards.ParameterError("NOVERLAP_FACTOR", "Must be a number greater than 0 and less than or equal to 1")
			if not(isinstance(self.DETREND[key], str)) or self.NOVERLAP_FACTOR[key] not in ['linear', 'constant']:
				raise standards.ParameterError("DETREND", "Must be either 'linear' or 'constant'")
			