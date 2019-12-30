import numpy as np


def maxNormalize(data):
	max = np.max(data)
	return data / max
	
def probNormalize(data):
	sum = np.sum(data)
	return data / sum
	
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
		
def bandedSpectralEntropy(data, resolutions, bands):
	dataBands = computeBands(data, resolution, bands)
	normDataBands = probNormalize(dataBands)
	entropy = np.sum(normDataBands*np.log(1/normDataBands))
	return entropy