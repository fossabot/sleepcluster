"""Normalizers"""

# Authors: Jeffrey Wang
# License: BSD 3 clause

import numpy as np


def max_normalize(data, scale=(0,1)):
	if np.max(data) - np.min(data) == 0:
		return data * scale[1]
	else:
		return ((data - np.min(data)) * (scale[1] - scale[0])) / (np.max(data) - np.min(data)) + scale[0]

def prob_normalize(data, scale=1):
	return (data / np.sum(data)) * scale

def log_normalize(data, base=np.e, scale=(0,1)):
	return maxNormalize(logTransform(data, base=base), scale=scale)
