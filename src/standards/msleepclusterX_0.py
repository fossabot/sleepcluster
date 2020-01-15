from standards import msleepclusterX as standards
from lib import data as dataLib

# A mSleepClusterX-type SleepCluster Standard
#	Build: 0
class mSleepClusterX_0(standards.mSleepClusterX):
	
	def __init__(self):
		self.NORMALIZER = dataLib.maxNormalize
		self.NORMALIZE_ARG = None
		self.EPOCH_SIZE = 5
		self.PERCENTILE = 95
		self.BANDS = [	(0.5, 3),
						(7, 9),
						(12, 15),
						(16, 40)
					]
		self.NPERSEG_FACTOR = { 'EEG':0.75, 'EMG1':0.75, 'EMG2':0.75 }
		self.NOVERLAP_FACTOR = { 'EEG':0.5, 'EMG1':0.5, 'EMG2':0.5 }
		self.DETREND = { 'EEG':'constant', 'EMG1':'constant', 'EMG2':'constant' }
	