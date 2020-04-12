"""Base Reader"""

# Authors: Jeffrey Wang
# License: BSD 3 clause

from abc import ABC, abstractmethod

# BaseReader defines the Class structure and necessary components
#	to a Data Importer
class BaseReader(ABC):
	standard = "unspecified files"
	filetypes = []

	def __init__(self, filepath):
		self.filepath = filepath

	def __str__(self):
		return type(self).__name__ + " at " + self.filepath

	@abstractmethod
	def read(self, *args, **kwargs):
		raise NotImplementedError( "No read function implemented" )
