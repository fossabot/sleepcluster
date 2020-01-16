import numpy as np
from math import floor
from tqdm import tqdm

from lib import data as dataLib
from processors import abstract_processor as processor
from dataobjects import dataobject as dataObject


# A Processor plugin for the msleepclusterX-type SleepCluster Standard 
class Processor_mSCX(processor.Processor):

	def __init__(self, parameters):
		self.parameters = parameters
		pass
		
	def process(self, channels={}):
		if channels.keys() != self.parameters.CHANNELS.keys():
			raise RuntimeError("Channels do not comply with standards")
		for key in self.parameters.CHANNELS.keys():
			if len(channels[key]) != self.parameters.CHANNELS[key]:
				raise RuntimeError("Channels do not comply with standards")
			for el in channels[key]:
				if not(isinstance(el, dataObject.DataObject)):
					raise RuntimeError("Channels do not comply with standards")
		
		headers = self.formatHeaders()
		data = []
		
		EPOCH_DATA = {}

		for key in channels.keys():
			EPOCH_DATA[key] = []
			for i in range(len(channels[key])):
				channels[key][i] = channels[key][i].process(self.parameters.NORMALIZER[key], self.parameters.NORMALIZE_ARG[key])
				EPOCH_DATA[key].append(self.calculateEpochs(channels[key][i], epoch_size=self.parameters.EPOCH_SIZE))
		
		num_epochs = []
		for key in EPOCH_DATA.keys():
			for channel in EPOCH_DATA[key]:
				num_epochs.append(channel['epochs'])
		num_epochs = min(num_epochs)
	
		for i in tqdm(range(num_epochs)):
		
			features = {}
			for feature in self.parameters.FEATURES:
				features[feature] = { 'merge': self.parameters.FEATURES[feature]['merge'] }
		
			for key in channels.keys():
				for feature in features.keys():
					features[feature][key] = []
				
				for j in range(len(channels[key])):
					epoch = channels[key][j].getData(i*EPOCH_DATA[key][j]['size'], k=(i+1)*EPOCH_DATA[key][j]['size'])

					fs = 1/channels[key][j].resolution
					nperseg = fs * self.parameters.NPERSEG_FACTOR[key]
					noverlap = nperseg * self.parameters.NOVERLAP_FACTOR[key]
					f, Pxx = dataLib.welch(epoch, fs=fs, nperseg=nperseg, noverlap=noverlap,
											detrend=self.parameters.DETREND[key])
					
					if self.parameters.FEATURES['0.BANDS'][key]:
						features['0.BANDS'][key].append(dataLib.computeBands(f, Pxx, self.parameters.FEATURES['0.BANDS'][key]))
					if self.parameters.FEATURES['1.ENTROPY'][key]:
						features['1.ENTROPY'][key].append(dataLib.simpleSpectralEntropy(f, Pxx))
					if self.parameters.FEATURES['2.RMS'][key]:
						features['2.RMS'][key].append(dataLib.rms(epoch))
					if self.parameters.FEATURES['3.PERCENTILE'][key]:
						features['3.PERCENTILE'][key].append(dataLib.percentileMean(epoch, self.parameters.FEATURES['3.PERCENTILE'][key]))
					if self.parameters.FEATURES['4.MEAN'][key]:
						features['4.MEAN'][key].append(np.mean(epoch))
			
			features = self.mergeFeatures(features)	
			data_row = [i] + self.formatFeatures(features)
			data.append(data_row)
		np_data = np.array(data)
		np_headers = np.array(headers)
		return {'headers': headers, 'data':np_data}
	
	def formatHeaders(self):
		headers = ['Epoch']
		features = sorted(self.parameters.FEATURES.keys())
		for f in features:
			keys = sorted(self.parameters.FEATURES[f].keys())
			for key in keys:
				if key != 'merge':
					if isinstance(self.parameters.FEATURES[f][key], list):
						for i in range(len(self.parameters.FEATURES[f][key])):
							headers.append(f+':'+key+'-'+str(i))
					else:
						headers.append(f+':'+key)
		return headers
	
	def calculateEpochs(self, channel, epoch_size=5):
		size = floor(epoch_size / channel.resolution)
		epochs = floor(channel.length / size)
		epoch_data = { 'size':size, 'epochs':epochs }
		return epoch_data
		
	def mergeFeatures(self, features):
		for f in features.keys():
			for key in features[f].keys():
				if key != 'merge' and len(features[f][key]) > 1:
					if features[f]['merge'] == 'MEAN':
						features[f][key] = np.mean(features[f][key], axis=0)
					elif features[f]['merge'] == 'MAX':
						features[f][key] = np.amax(features[f][key], axis=0)
		return features

	def formatFeatures(self, featureData):
		data_row = []
		features = sorted(self.parameters.FEATURES.keys())
		for f in features:
			keys = sorted(self.parameters.FEATURES[f].keys())
			for key in keys:
				if key != 'merge':
					if isinstance(featureData[f][key], list):
						for el in featureData[f][key]:
							data_row.append(el)
					elif isinstance(featureData[f][key], float):
						data_row.append(featureData[f][key])
		return data_row