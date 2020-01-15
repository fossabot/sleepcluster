import numpy as np
from math import floor
from tqdm import tqdm

from lib import data as dataLib
from processors import abstract_processor as processor


# A Processor plugin for the Parameters1-type SleepCluster Standard 
class Processor1(processor.Processor):

	def __init__(self, parameters):
		self.parameters = parameters
		pass
		
	def process(self, EEG=None, EMG1=None, EMG2=None):
		headers = np.array([['Epoch','EEG PS1','EEG PS2','EEG PS3','EEG PS4',
					'rmsEMG','T-F entropy EEG','T-F entropy EMG',
					'EMG95%mean','EMGmean'
					]])
		data = []

		EEG = EEG.process(self.parameters.NORMALIZER, self.parameters.NORMALIZE_ARG)
		EMG1 = EMG1.process(self.parameters.NORMALIZER, self.parameters.NORMALIZE_ARG)
		EMG2 = EMG2.process(self.parameters.NORMALIZER, self.parameters.NORMALIZE_ARG)		
		epoch_data = self.calculateEpochs(epoch_size=self.parameters.EPOCH_SIZE, EEG=EEG, EMG1=EMG1, EMG2=EMG2)
		num_epochs = floor(min([epoch_data['EEG_epochs'], epoch_data['EMG1_epochs'], epoch_data['EMG2_epochs']]))
		for i in tqdm(range(num_epochs)):
			EEGepoch = EEG.getData(i*epoch_data['EEG_size'], k=(i+1)*epoch_data['EEG_size'])
			EMG1epoch = EMG1.getData(i*epoch_data['EMG1_size'], k=(i+1)*epoch_data['EMG1_size'])
			EMG2epoch = EMG2.getData(i*epoch_data['EMG2_size'], k=(i+1)*epoch_data['EMG2_size'])
			
			EEGbands = dataLib.computeBands(EEGepoch, EEG.resolution, self.parameters.BANDS)
			
			rmsEMG = self.mergeRMS(EMG1epoch, EMG2epoch)
			
			EEGentropy = dataLib.bandedSpectralEntropy(EEGepoch, EEG.resolution, self.parameters.BANDS)
			EMG1entropy = dataLib.bandedSpectralEntropy(EMG1epoch, EMG1.resolution, self.parameters.BANDS)
			EMG2entropy = dataLib.bandedSpectralEntropy(EMG2epoch, EMG2.resolution, self.parameters.BANDS)
			EMGentropy = max(EMG1entropy, EMG2entropy)
						
			EMGpercentile = self.mergePercentileMean(EMG1epoch, EMG2epoch, self.parameters.PERCENTILE)
			EMGmean = self.mergeMean(EMG1epoch, EMG2epoch)
			
			data_row = [i]
			for band in EEGbands:
				data_row.append(band)
			data_row += [rmsEMG, EEGentropy, EMGentropy, EMGpercentile, EMGmean]
			data.append(data_row)
		np_data = np.array(data)
		return {'headers': headers, 'data':np_data}
	
	
	def calculateEpochs(self, epoch_size=5, EEG=None, EMG1=None, EMG2=None):
		epoch_data = {
						'EEG_size': floor(epoch_size / EEG.resolution),
						'EMG1_size': floor(epoch_size / EMG1.resolution),
						'EMG2_size': floor(epoch_size / EMG2.resolution)
					}
		epoch_data['EEG_epochs'] = floor(EEG.length / epoch_data['EEG_size'])
		epoch_data['EMG1_epochs'] = floor(EMG1.length / epoch_data['EMG1_size'])
		epoch_data['EMG2_epochs'] = floor(EMG2.length / epoch_data['EMG2_size'])
		return epoch_data

	def mergeRMS(self, d1, d2):
		d1rms = dataLib.rms(d1)
		d2rms = dataLib.rms(d2)
		return np.maximum(d1rms, d2rms)
	
	def mergePercentileMean(self, d1, d2, k):
		return np.mean([dataLib.percentileMean(d1, k), dataLib.percentileMean(d2, k)])
	
	def mergeMean(self, d1, d2):
		return np.mean([np.mean(d1), np.mean(d2)])