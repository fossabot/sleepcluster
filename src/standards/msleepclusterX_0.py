from standards import parameters1 as standards
from lib import data as dataLib

# A mSleepClusterX-type SleepCluster Standard
#	Build: 0
class mSleepClusterX_0(standards.mSleepClusterX):
	
	def __init__(self):
		self.NORMALIZER = dataLib.maxNormalize
		self.parameters.NORMALIZE_ARG = None
		self.EPOCH_SIZE = 5
		self.PERCENTILE = 95
		self.BANDS = [	(0.5, 3),
						(6, 9),
						(11, 15),
						(16, 40)
					]
		self.NPERSEG_FACTOR = { 'EEG':1, 'EMG1':1, 'EMG2':1 }
		self.NOVERLAP_FACTOR = { 'EEG':0.5, 'EMG1':0.5, 'EMG2':0.5 }
		self.DETREND = { 'EEG':'linear', 'EMG1':'linear', 'EMG2':'linear' }
	