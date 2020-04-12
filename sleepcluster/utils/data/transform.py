"""Transformers"""

# Authors: Jeffrey Wang
# License: BSD 3 clause

import numpy as np
from scipy import stats


def log_transform(data, base=np.e):
	return np.log(data) / np.log(base)

def boxcox_transform(data):
	return stats.boxcox(data)

def power_scale(data, a):
	return np.sign(data) * np.power(np.absolute(data), a)
