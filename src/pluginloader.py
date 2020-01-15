import sys, os
from importlib.machinery import SourceFileLoader


# Load all plugins specified
#	To install a plugin, add the following before after line 11
#		modules.append(getattr(SourceFileLoader("[pluginName]", "./plugins/[pluginName].py").load_module(), "[pluginName]"))
def loadPlugins():
	reader_mods = []
	reader_mods.append(SourceFileLoader("smrMATreader", "./dataobjects/smrMATreader.py").load_module())
	processor_mods = []
	processor_mods.append(SourceFileLoader("processor1", "./processors/processor1.py").load_module())
	standards_mods = []
	standards_mods.append(SourceFileLoader("msleepclusterX_0", "./standards/msleepclusterX_0.py").load_module())
	return {'readers':reader_mods, 'processors':processor_mods, 'standards':standards_mods}