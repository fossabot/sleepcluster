import sys, os
from importlib.machinery import SourceFileLoader

# Easy reading of plugins installed - not actually used
plugins = ['smrMAT']

# Load all plugins specified
#	To install a plugin, add the following before after line 11
#		modules.append(getattr(SourceFileLoader("[pluginName]", "./plugins/[pluginName].py").load_module(), "[pluginName]"))
def loadPlugins():
	modules = []
	modules.append(getattr(SourceFileLoader("smrMAT", "./dataobjects/smrMAT.py").load_module(), "smrMAT"))
	return modules