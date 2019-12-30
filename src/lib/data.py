import numpy as np


def normalize(data):
	max = np.max(data)
	return data / max
	
def computeBands(data, resolution, bands):
	fft_vals = np.square(np.fft.rfft(data))
	fft_freq = np.fft.rfftfreq(len(data), resolution)
	dataBands = []
	for band in bands:
		freq_ix = np.where((fft_freq >= eeg_bands[band][0]) & (fft_freq <= eeg_bands[band][1]))[0]
		dataBands.append(np.mean(fft_vals[freq_ix]))
	return dataBands
	
def rms(data):
	return np.sqrt(np.mean(np.square(data)))
	
def zeroCross(data):
	return ((data[:-1] * data[1:]) < 0).sum()
	
def percentileMean(data, k):
	index = (len(data)*k)//100
	return np.mean(np.partition(data, index)[index:])
		
def spectralEntropy(data):
		
	
	return