# The smrMATData Import Type Standard

This is a Data Import Type Standard that uses .mat files in the format as exported
by Spike2 v7.

The underlying data structure of the dataset is as follows:
1. The data structure is a dictionary with key-value pairs
2. The overall file contains Channels, each named as [title]_Ch[X]
	1. This is found in the keys of the data structure, e.g. data[channel]
3. At least ONE channel contains the EMG/EEG data to be analyzed
	1. A "title" which contains the name of the channel
		1. This is found in data[channel][0][0][0][0]
	2. A "resolution" of the channel recording, containing the time resolutionof the recording in seconds
		1. This is found in data[channel][0][0][2][0][0]
	3. A "length" of the channel recording, containing the number of samples
		1. This is found in data[channel][0][0][7][0][0]
	4. A "data-stream" of the channel recording, containing the actual samples
		1. This is found in data[channel][0][0][8]
