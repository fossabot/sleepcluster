from importlib.machinery import SourceFileLoader
standards = SourceFileLoader("standards", "./standards/abstract_standards.py").load_module()

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

class Parameters1(standards.Standards):
	
	def __init__(self):
		self.bands = [	(0, 4),
						(4, 9),
						(11, 15),
						(15, 40)
					]
		
	def validateParameters():
		raise NotImplementedError( "No validateParameters function implemented" )	
	