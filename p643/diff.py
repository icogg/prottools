def _myround(x, base=5):
	return base * round(float(x) / base)

def tapspill(hv=[], lv=[], tv=[]):
	"""Calculates the maximum error created by tap changers on the transfomer
	Input where fitted:
			hv = [max voltage, min voltage]
			lv = [max voltage, min voltage]
			tv = [max voltage, min voltage]
	
	Output
			spill in per unit
	"""
	if len(hv)==2:
		hverror = max(hv) / (((max(hv) - min(hv)) / 2 + min(hv))) - 1
	else:
		hverror = 0
 
	if len(lv)==2:
		lverror = max(lv) / (((max(lv) - min(lv)) / 2 + min(lv))) - 1 
	else:
		lverror = 0
		
	if len(tv)==2:
		tverror = max(tv) / (((max(tv) - min(tv)) / 2 + min(tv))) - 1
	else:
		tverror = 0

	taperror = max([hverror + lverror, lverror + tverror, tverror + hverror])
	
	return taperror



def biaseddiff(hv=[],lv=[],tv=[],relayerror=5,excitationerror=3,cterror=5):
	try:
		relayerror = relayerror / 100
		excitationerror = excitationerror / 100
		cterror = cterror / 100
	except:
		return print ('input error')
	
	taperror = tapspill(hv,lv,tv)
	
	k1 = (1 + cterror) - ((1 - cterror) / (1 + taperror)) + relayerror + excitationerror
	
	k1 = _myround(max(k1, 0.2), 0.05)
	
	k2 = 0.8
	
	Is2 = 1
	
	return {'k1': k1, 'k2': k2, 'Is2': Is2}
