import numpy as np

def var3ph(Vline, Iline):
	"""returns the power for a three phase system for a given line voltage and
	current
	"""
	return np.sqrt(3) * Vline * Iline


def Inom(VA, Vline, threephase=True):
	"""returns the phase current in amperes for a given VA and Voltage
	the function returns the current based on a three phase calculation. If single
	phase is required set threephase = False
	"""
	if threephase:
		return VA / (np.sqrt(3) * Vline)
	else:
		return VA / Vline


	
	
