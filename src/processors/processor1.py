import numpy as np

from lib import data as dataLib
from processors import abstract_processor as processor


# A Processor plugin for the Parameters1-type SleepCluster Standard 
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
		EEG = eeg.process(self.parameters.NORMALIZER)
		EMG1 = emg1.process(self.parameters.NORMALIZER)
		EMG2 = emg2.process(self.parameters.NORMALIZER)
		epoch_data = calculateEpochs(epoch_size=self.parameters.EPOCH_SIZE, EEG=EEG, EMG1=EMG1, EMG2=EMG2)
		num_epochs = min([epoch_data['eeg_epochs'], epoch_data['emg1_epochs'], epoch_data['emg2_epochs']])
		for i in range(num_epochs):
			EEGepoch = eeg.getData(i*epoch_data['EEG_size'], k=(i+1)*epoch_data['EEG_size'])
			EMG1epoch = emg1.getData(i*epoch_data['EMG1_size'], k=(i+1)*epoch_data['EMG1_size'])
			EMG2epoch = emg2.getData(i*epoch_data['EMG2_size'], k=(i+1)*epoch_data['EMG2_size'])
			
			EEGbands = dataLib.computeBands(EEGepoch, EEG.resolution, self.parameters.BANDS)
			
			rmsEMG = self.mergeRMS(EMG1epoch, EMG2epoch)
			
			EEGentropy = dataLib.bandedSpectralEntropy(EEGepoch, EEG.resolution, self.parameters.BANDS)
			EMG1entropy = dataLib.bandedSpectralEntropy(EMG1epoch, EMG1.resolution, self.parameters.BANDS)
			EMG2entropy = dataLib.bandedSpectralEntropy(EMG2epoch, EMG2.resolution, self.parameters.BANDS)
			EMGentropy = max(EMG1entropy, EMG2entropy)
			'''
			zerocross = dataLib.zeroCross(EEGepoch)
			
			EMGpercentile = self.mergePercentileMean(EMG1epoch, EMG2epoch, self.parameters.PERCENTILE)
			EMGmean = self.mergeMean(EMG1epoch, EMG2epoch)
			'''
			data_row = [i]
			for band in EEGbands:
				data_row.append(band)
			data_row + [rmsEMG, EEGentropy, EMGentropy, zerocross, EMGpercentile, EMGmean]
			data.append(data_row)
		np_data = np.array(data)
		return {'headers': headers, 'data':np_data}
	
	
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

	def mergeRMS(self, d1, d2):
		d1rms = dataLib.rms(d1)
		d2rms = dataLib.rms(d2)
		return np.maximum(d1rms, d2rms)
	
	def mergePercentileMean(self, d1, d2, k):
		return np.mean(dataLib.percentileMean(d1, k), dataLib.percentileMean(d2, k))
	
	def mergeMean(self, d1, d2):
		return np.mean(np.mean(d1), np.mean(d2))