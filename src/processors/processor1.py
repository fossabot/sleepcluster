from importlib.machinery import SourceFileLoader
processor = SourceFileLoader("processor", "./processors/abstract_processor.py").load_module()
parameters = SourceFileLoader("processor", "./processors/abstract_processor.py").load_module()

import numpy as np

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
 - Max entropy between two EMG channels

Zero Crossings on EEG
 - On the Moving Average
 - On absolute Zero

EMG 95% mean amplitude on both
EMG mean amplitude on both
'''

# A Processor plugin
class Processor1(processor.Processor):

	def __init__(self, parameters):
		self.parameters = parameters
		pass
		
	def process(self, EEG=None, EMG1=None, EMG2=None):
		headers = np.array([['Epoch','EEG PS(1-4)','EEG PS(5-9)','EEG PS(11-15)','EEG PS(16-40)',
					'rmsEMG','T-F entropy EEG','T-F entropy EMG','ZeroCross EEG',
					'EMG95%mean','EMGmean'
					]])
		data = []
		EEG = eeg.process(self.normalize)
		EMG1 = emg1.process(self.normalize)
		EMG2 = emg2.process(self.normalize)
		epoch_data = calculateEpochs(EEG=EEG,EMG1=EMG1,EMG2=EMG2)
		num_epochs = min([epoch_data['eeg_epochs'], epoch_data['emg1_epochs'], epoch_data['emg2_epochs']])
		for i in range(num_epochs):
			EEGepoch = eeg.getData(i*epoch_data['EEG_size'], k=(i+1)*epoch_data['EEG_size'])
			EMG1epoch = emg1.getData(i*epoch_data['EMG1_size'], k=(i+1)*epoch_data['EMG1_size'])
			EMG2epoch = emg2.getData(i*epoch_data['EMG2_size'], k=(i+1)*epoch_data['EMG2_size'])
			
			EEGbands = self.computeBands(EEGepoch, EEG.resolution, self.parameters.bands)
			
			rmsEMG = self.mergeRMS(EMG1epoch, EMG2epoch)
			
			# tf spectral entropy
			
			zerocross = self.zeroCross(EEGepoch)
			
			EMGpercentile = self.mergePercentileMean(EMG1epoch, EMG2epoch, 95)
			EMGmean = self.mergeMean(EMG1epoch, EMG2epoch)
			data.append([])
		np_data = np.array(data)
		return {'headers': headers, 'data':np_data}
		
	def normalize(self, data):
		max = np.max(data)
		return data / max
	
	def calculateEpochs(self, epoch_size=5, EEG=None, EMG1=None, EMG2=None):
		epoch_data = {
						'EEG_size': EEG.length * EEG.resolution,
						'EMG1_size': EMG1.length * EMG1.resolution,
						'EMG2_size': EMG2.length * EMG2.resolution
					}
		epoch_data['EEG_epochs'] = epoch_data['EEG_size'] // epoch_size
		epoch_data['EMG1_epochs'] = epoch_data['EMG1_size'] // epoch_size
		epoch_data['EMG2_epochs'] = epoch_data['EMG2_size'] // epoch_size
		return epoch_data
		
	def computeBands(self, data, resolution, bands):
		fft_vals = np.square(np.fft.rfft(data))
		fft_freq = np.fft.rfftfreq(len(data), resolution)
		dataBands = []
		for band in bands:
			freq_ix = np.where((fft_freq >= eeg_bands[band][0]) & (fft_freq <= eeg_bands[band][1]))[0]
			dataBands.append(np.mean(fft_vals[freq_ix]))
		return dataBands
		
	def mergeRMS(self, d1, d2):
		d1rms = rms(d1)
		d2rms = rms(d2)
		return np.maximum(d1rms, d2rms)
		
	def rms(self, data):
		return np.sqrt(np.mean(data**2))
	
	def zeroCross(self, data):
		return ((data[:-1] * data[1:]) < 0).sum()
		
	def mergePercentileMean(self, d1, d2, k):
		return np.mean(self.percentileMean(d1, k), self.percentileMean(d2, k))
	
	def mergeMean(self, d1, d2):
		return np.mean(np.mean(d1), np.mean(d2))
		
	def percentileMean(self, data, k):
		index = (len(data)*k)//100
		return np.mean(np.partition(data, index)[index:])