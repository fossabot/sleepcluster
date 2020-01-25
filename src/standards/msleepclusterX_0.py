from standards import msleepclusterX as standards
from lib import data as dataLib

# A mSleepClusterX-type SleepCluster Standard
#	Build: 0
class mSleepClusterX_0(standards.mSleepClusterX):

	def __init__(self):
		self.CHANNELS = {
							'EEG':1,
							'EMG':2
						}
		self.EPOCH_SIZE = 5

		self.NORMALIZER = 		{	'EEG': dataLib.maxNormalize, 	'EMG': dataLib.maxNormalize }
		self.NORMALIZE_ARG = 	{ 	'EEG': None, 					'EMG': None 				}

		self.NPERSEG_FACTOR = 	{ 	'EEG': 0.75,		'EMG': 0.75			}
		self.NOVERLAP_FACTOR = 	{ 	'EEG': 0.5, 		'EMG': 0.5 			}
		self.DETREND = 			{ 	'EEG': 'constant', 	'EMG': 'constant' 	}

		self.FEATURES = {
							'0.BANDS':			{
													'EEG': [	(0.5, 4), 	(7, 9), 	(11, 40)	],
													'EMG': None,
													'merge': 'MEAN'
												},
							'1.ENTROPY': 		{ 	'EEG': True,	'EMG': False, 	'merge': 'MAX' 	},
							'2.RMS': 			{ 	'EEG': False,	'EMG': False, 	'merge': 'MAX' 	},
							'3.PERCENTILE': 	{ 	'EEG': None, 	'EMG': 95, 		'merge': 'MEAN'	},
							'4.MEAN':			{ 	'EEG': False, 	'EMG': False, 	'merge': 'MEAN'	}
						}
