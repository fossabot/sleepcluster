#DO NOT change any parameter names




#Validation Function
#DO NOT edit

class ParameterError(Exception):
	def __init__(self, parameter, message):
		self.parameter = parameter
		self.message = message
		

def validateParameters():

	return True