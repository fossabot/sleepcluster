import numpy as np
from scipy import signal
from scipy import stats

def maxNormalize(data, scale=(0,1)):
	if np.max(data) - np.min(data) == 0:
		return data * scale[1]
	else:
		return ((data - np.min(data)) * (scale[1] - scale[0])) / (np.max(data) - np.min(data)) + scale[0]

def probNormalize(data, scale=1):
	return (data / np.sum(data)) * scale

def powerScale(data, a):
	return np.sign(data) * np.power(np.absolute(data), a)

def logNormalize(data, base=np.e, scale=(0,1)):
	return maxNormalize(logTransform(data, base=base), scale=scale)

def logTransform(data, base=np.e):
	return np.log(data) / np.log(base)

def boxCoxTransform(data):
	return stats.boxcox(data)

def movingAverage(data, window, weights=None):
	result = []
	for i in range(len(data)):
		if i - window < 0:
			start = 0
		else:
			start = i - window
		if weights:
			sum = np.sum(data[start:i+1] * weights)
		else:
			sum = np.sum(data[start:i+1])
		result.append(sum / (i-start+1))
	return np.array(result)

def hullMovingAverage(data, window, weights=None):
	period = int(np.sqrt(window))
	half = int(window / 2)
	if weights:
		halfaverage = movingAverage(data, half, weights[:half])
		fullaverage = movingAverage(data, window, weights)
		intermediate = 2 * halfaverage - fullaverage
		result = movingAverage(intermediate, period, weights[:period])
	else:
		halfaverage = movingAverage(data, half)
		fullaverage = movingAverage(data, window)
		intermediate = 2 * halfaverage - fullaverage
		result = movingAverage(intermediate, period)
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
