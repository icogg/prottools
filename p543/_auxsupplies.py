def dcinputs(DCNominal=110):
	"""Enter the substation nominal voltage eg DCNominal = 48
	Return the required setting for the MiCOM Px4x platform"""
	result = 'Not Valid'
	if DCNominal >= 220:
		result = '220/250V'
	elif DCNominal >= 110:
		result = '110/125V'
	elif DCNominal >= 48:
		result ='48/54V'
	elif DCNominal >= 30:
		result = '30/34V'
	elif DCNominal >= 24:
		result = '24/27V'
	else:
		result = 'Check'
	return {'Global Nominal DC':result}
