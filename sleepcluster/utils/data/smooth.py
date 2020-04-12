"""Smoothing Functions"""

# Authors: Jeffrey Wang
# License: BSD 3 clause

import numpy as np


def moving_average(data, window, weights=None):
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

def hull_moving_average(data, window, weights=None):
	period = int(np.sqrt(window))
	half = int(window / 2)
	if weights:
		halfaverage = moving_average(data, half, weights[:half])
		fullaverage = moving_average(data, window, weights)
		intermediate = 2 * halfaverage - fullaverage
		result = moving_average(intermediate, period, weights[:period])
	else:
		halfaverage = moving_average(data, half)
		fullaverage = moving_average(data, window)
		intermediate = 2 * halfaverage - fullaverage
		result = moving_average(intermediate, period)
	return result
