import sys, os
from importlib.machinery import SourceFileLoader

# Easy reading of plugins installed - not actually used
plugins = [
			'smrMAT',
			'processor1',
			'parameters1'
		]

# Load all plugins specified
#	To install a plugin, add the following before after line 11
#		modules.append(getattr(SourceFileLoader("[pluginName]", "./plugins/[pluginName].py").load_module(), "[pluginName]"))
def loadPlugins():
	modules = []
	modules.append(SourceFileLoader("smrMATreader", "./dataobjects/smrMATreader.py").load_module())
	modules.append(SourceFileLoader("processor1", "./processors/processor1.py").load_module())
	modules.append(SourceFileLoader("parameters1", "./standards/parameters1.py").load_module())
	return modules