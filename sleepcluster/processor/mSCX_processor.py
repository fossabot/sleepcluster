"""mSleepClusterX Processor"""

# Authors: Jeffrey Wang
# License: BSD 3 clause

import numpy as np
from math import floor

from . import BaseProcessor
from ..utils.data import normalize, smooth, transform, signal
from ..utils import DataObject


# A Processor plugin for the msleepclusterX-type SleepCluster Standard
class mSCXprocessor(BaseProcessor):

	def __init__(self, standards):
		self.standards = standards
		pass

	def compliance(self, channels={}):
		if channels.keys() != self.standards.CHANNELS.keys():
			raise RuntimeError("Channels do not comply with standards")
		for key in self.standards.CHANNELS.keys():
			if len(channels[key]) != self.standards.CHANNELS[key]:
				raise RuntimeError("Channels do not comply with standards")
			for el in channels[key]:
				if not(isinstance(el, DataObject)):
					raise RuntimeError("Channels do not comply with standards")

	def process(self, channels={}):
		self.compliance(channels=channels)
		headers = self.format_headers()
		data = []

		EPOCH_DATA = {}

		for key in channels.keys():
			EPOCH_DATA[key] = []
			for i in range(len(channels[key])):
				channels[key][i] = channels[key][i].process(self.standards.NORMALIZER[key], self.standards.NORMALIZE_ARG[key])
				EPOCH_DATA[key].append(self.calculate_epochs(channels[key][i], epoch_size=self.standards.EPOCH_SIZE))

		num_epochs = []
		for key in EPOCH_DATA.keys():
			for channel in EPOCH_DATA[key]:
				num_epochs.append(channel['epochs'])
		num_epochs = min(num_epochs)

		for i in range(num_epochs):

			features = {}
			for feature in self.standards.FEATURES:
				features[feature] = { 'merge': self.standards.FEATURES[feature]['merge'] }

			for key in channels.keys():
				for feature in features.keys():
					features[feature][key] = []

				for j in range(len(channels[key])):
					epoch = channels[key][j].getData(i*EPOCH_DATA[key][j]['size'], k=(i+1)*EPOCH_DATA[key][j]['size'])

					fs = 1/channels[key][j].resolution
					nperseg = fs * self.standards.NPERSEG_FACTOR[key]
					noverlap = nperseg * self.standards.NOVERLAP_FACTOR[key]
					f, Pxx = signal.welch(epoch, fs=fs, nperseg=nperseg, noverlap=noverlap,
											detrend=self.standards.DETREND[key])

					if self.standards.FEATURES['0.BANDS'][key]:
						bands = signal.compute_bands(f, Pxx, self.standards.FEATURES['0.BANDS'][key])
						features['0.BANDS'][key].append(bands[1]/bands[0])
					if self.standards.FEATURES['1.ENTROPY'][key]:
						features['1.ENTROPY'][key].append(singal.spectral_entropy(f, Pxx))
					if self.standards.FEATURES['2.RMS'][key]:
						features['2.RMS'][key].append(signal.rms(epoch))
					if self.standards.FEATURES['3.PERCENTILE'][key]:
						features['3.PERCENTILE'][key].append(signal.percentile_mean(epoch, self.standards.FEATURES['3.PERCENTILE'][key]))
					if self.standards.FEATURES['4.MEAN'][key]:
						features['4.MEAN'][key].append(np.mean(epoch))

			features = self.merge_features(features)
			data_row = self.format_features(features)
			data.append(data_row)
		np_data = np.array(data)

		np_data = np_data.T
		for col in range(len(np_data)):
			np_data[col] = normalize.max_normalize(np_data[col], scale=(5,10))
			np_data[col] = smooth.hull_moving_average(np_data[col], 4)
			np_data[col] = transform.log_transform(np_data[col], np.median(np_data[col]))
		np_data = np_data.T

		np_headers = np.array([headers])
		return {'headers': np_headers, 'data':np_data}

	def format_headers(self):
		headers = []
		features = sorted(self.standards.FEATURES.keys())
		for f in features:
			keys = sorted(self.standards.FEATURES[f].keys())
			for key in keys:
				if key != 'merge' and self.standards.FEATURES[f][key] not in [False, None]:
					if isinstance(self.standards.FEATURES[f][key], list) and f == '0.BANDS':
						headers.append(f+':'+key)
					elif isinstance(self.standards.FEATURES[f][key], list):
							for i in range(len(self.standards.FEATURES[f][key])):
								headers.append(f+':'+key+'-'+str(i))
					else:
						headers.append(f+':'+key)
		return headers

	def calculate_epochs(self, channel, epoch_size=5):
		size = floor(epoch_size / channel.resolution)
		epochs = floor(channel.length / size)
		epoch_data = { 'size':size, 'epochs':epochs }
		return epoch_data

	def merge_features(self, features):
		for f in features.keys():
			for key in features[f].keys():
				if key != 'merge' and len(features[f][key]) >= 1:
					if features[f]['merge'] == 'MEAN':
						features[f][key] = np.mean(features[f][key], axis=0)
					elif features[f]['merge'] == 'MAX':
						features[f][key] = np.amax(features[f][key], axis=0)
		return features

	def format_features(self, featureData):
		data_row = []
		features = sorted(self.standards.FEATURES.keys())
		for f in features:
			keys = sorted(self.standards.FEATURES[f].keys())
			for key in keys:
				if key != 'merge' and self.standards.FEATURES[f][key] not in [False, None]:
					if isinstance(featureData[f][key], np.ndarray):
						for el in featureData[f][key]:
							data_row.append(el)
					elif isinstance(featureData[f][key], float):
						data_row.append(featureData[f][key])
		return data_row
