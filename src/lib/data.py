import numpy as np
#from scipy.integrate import simps
#from mne.time_frequency import psd_array_multitaper
from scipy import signal

def maxNormalize(data, scale=(0,1)):
	if np.max(data) - np.min(data) == 0:
		return (data * (scale[1] - scale[0])) / data + scale[0]
	else:
		return ((data - np.min(data)) * (scale[1] - scale[0])) / (np.max(data) - np.min(data)) + scale[0]
	
def probNormalize(data, scale=1):
	return (data / np.sum(data)) * scale
	
def powerScale(data, a):
	return np.sign(data) * np.power(np.absolute(data), a)
	
def logNormalize(data):
	return maxNormalize(np.log(data + np.absolute(np.min(data)) + 1))
	
def smoothMovingAverage(data, window):
	half = window // 2
	result = []
	for i in range(len(data)):
		if i - half < 0:
			start = 0
		else:
			start = i + half
		if i + window - half >= len(data):
			end = len(data)
		else:
			end = i + window - half
		sum = np.sum(data[start:end])
		result.append(sum/(end-start))
	return result
	
def computeBands(f, Pxx, bands):
	dataBands = []
	for band in bands:
		f_ix = np.where((f >= band[0]) & (f <= band[1]))[0]
		dataBands.append(np.mean(Pxx[f_ix]))
	return dataBands
	
def welch(data, fs=1.0, nperseg=None, noverlap=None, nfft=None, detrend='constant'):
	f, Pxx = signal.welch(data, fs=fs, nperseg=nperseg, noverlap=noverlap, 
							nfft=nfft, detrend=detrend, return_onesided=True, scaling='spectrum')
	return f, Pxx
		
def simpleSpectralEntropy(f, Pxx):
	norm_Pxx = probNormalize(Pxx)
	entropy = np.sum(norm_Pxx*np.log(1/norm_Pxx))
	normEntropy = entropy / np.log(len(f))
	return normEntropy
	
def rms(data):
	return np.sqrt(np.mean(np.square(data)))
	
def zeroCross(data, zero=0):
	return ((data[:-1] * data[1:]) < zero).sum()
	
def percentileMean(data, k):
	index = (len(data)*k)//100
	return np.mean(np.partition(data, index)[index:])