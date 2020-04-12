"""Exceptions and Warnings"""

# Authors: Jeffrey Wang
# License: BSD 3 clause

# Exception defined by an invalid parameter
class ParameterError(Exception):
	def __init__(self, parameter, message):
		self.parameter = parameter
		self.message = message
