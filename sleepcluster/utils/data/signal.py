"""Signal Processing Functions"""

# Authors: Jeffrey Wang
# License: BSD 3 clause

import numpy as np
from scipy import signal


def compute_bands(f, Pxx, bands):
	dataBands = []
	for band in bands:
		f_ix = np.where((f >= band[0]) & (f <= band[1]))[0]
		dataBands.append(np.mean(Pxx[f_ix]))
	return dataBands

def welch(data, fs=1.0, nperseg=None, noverlap=None, nfft=None, detrend='constant'):
	f, Pxx = signal.welch(data, fs=fs, nperseg=nperseg, noverlap=noverlap,
							nfft=nfft, detrend=detrend, return_onesided=True, scaling='spectrum')
	return f, Pxx

def spectral_entropy(f, Pxx):
	norm_Pxx = probNormalize(Pxx)
	entropy = np.sum(norm_Pxx*np.log(1/norm_Pxx))
	normEntropy = entropy / np.log(len(f))
	return normEntropy

def rms(data):
	return np.sqrt(np.mean(np.square(data)))

def zero_cross(data, zero=0):
	return ((data[:-1] * data[1:]) < zero).sum()

def percentile_mean(data, k):
	index = (len(data)*k)//100
	return np.mean(np.partition(data, index)[index:])
