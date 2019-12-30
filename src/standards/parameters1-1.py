from standards import parameters1 as standards
from lib import data as dataLib

'''
EEG Power Spectrum
1-4
5-9
11-15
16-40

rms EMG for both channels
 - Normalized against a "baseline" for each channel
 - Summated into one channel

Time-Frequency Balanced Spectral Entropy of EEG and EMG
 - Time windows? Longer windows for shorter frequencies

Moving Average on EEG

Zero Crossings on EEG
 - On the Moving Average
 - On absolute Zero

EMG max amplitude
EMG average amplitude
'''

class Parameters1_1(standards.Parameters1):
	
	def __init__(self):
		self.NORMALIZER = dataLib.normalize
		self.EPOCH_SIZE = 5
		self.PERCENTILE = 95
		self.BANDS = [	(0, 4),
						(4, 9),
						(11, 15),
						(15, 40)
					]
		
	def validateParameters():
		raise NotImplementedError( "No validateParameters function implemented" )	
	