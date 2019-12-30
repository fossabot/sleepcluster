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
		
	def process(self, eeg=None, emg1=None, emg2=None):
		headers = np.array([['Epoch','EEG PS(1-4)','EEG PS(5-9)','EEG PS(11-15)','EEG PS(16-40)',
					'rmsEMG','T-F entropy EEG','T-F entropy EMG','ZeroCross EEG',
					'EMG95%mean','EMGmean'
					]])
		eeg = eeg.process(normalize)
		emg1 = emg1.process(normalize)
		emg2 = emg2.process(normalize)
		epoch_data = calculateEpochs(eeg=eeg,emg1=emg1,emg2=emg2)
		num_epochs = min([epoch_data['eeg_epochs'], epoch_data['emg1_epochs'], epoch_data['emg2_epochs']])
		for i in range(num_epochs):
			eegepoch = eeg.getData(i*epoch_data['eeg_size'], k=(i+1)*epoch_data['eeg_size'])
			emg1epoch = emg1.getData(i*epoch_data['emg1_size'], k=(i+1)*epoch_data['emg1_size'])
			emg2epoch = emg2.getData(i*epoch_data['emg2_size'], k=(i+1)*epoch_data['emg2_size'])
			
			# power spec
			
			emg1rms = rms(emg1, emg1.resolution * 10)
			emg2rms = rms(emg2, emg2.resolution * 10)
			rmsEMG = np.maximum(emg1rms, emg2rms)
			
			# tf spectral entropy
			
			zerocross = ((eegepoch[:-1] * eegepoch[1:]) < 0).sum()
			
			EMG1idx95 = (len(emg1epoch)*95)//100
			EMG2idx95 = (len(emg2epoch)*95)//100
			EMG95mean = np.mean(np.mean(np.partition(emg1poch,EMG1idx95)[EMG1idx95:]),
								np.mean(np.partition(emg2epoch,EMG2idx95)[EMG2idx95:])))
			EMGmean = np.mean((np.mean(emg1epoch),np.mean(emg2epoch))
		np_data = np.array(data)
		return {'headers': headers, 'data':np_data}
		
	def calculateEpochs(self, epoch_size=5, eeg=None, emg1=None, emg2=None):
		epoch_data = {
						'eeg_size': eeg.length * eeg.resolution,
						'emg1_size': emg1.length * emg1.resolution,
						'emg2_size': emg2.length * emg2.resolution
					}
		epoch_data['eeg_epochs'] = epoch_data['eeg_size'] // epoch_size
		epoch_data['emg1_epochs'] = epoch_data['emg1_size'] // epoch_size
		epoch_data['emg2_epochs'] = epoch_data['emg2_size'] // epoch_size
		return epoch_data
	
	def normalize(self, data):
		max = np.max(data)
		return data / max
		
	def rms(self, data, n):
		rms = []
		for i in range(len(data)):
			start = i - n
			end = i + n
			if start < 0:
				start = 0
			if end >= len(data):
				end = len(data)-1
			window = data[start:end]
			rms.append(np.sqrt(np.mean(window**2)))
		return rms