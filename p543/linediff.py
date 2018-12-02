def diff(ends=2, kV=132, nF=0, LocalCT=[], Remote1CT=[], Remote2CT=[], freq=50):
	
	if ends==2:
		if len(LocalCT)==2 & len(Remote1CT)==2:
			pass
		else:
			return print('Local and Remote1 CT details required in form [Prim,Sec]')
		k2 = 150
		CTBase = min(_CT(LocalCT)['CTPrim'], _CT(Remote1CT)['CTPrim'])

	if ends==3:
		if len(LocalCT)==2 & len(Remote1CT)==2 & len(Remote2CT)==2:
			pass
		else:
			return print('Local and Remote(x) CT details required in form [Prim,Sec]')
		k2 = 100
		CTBase = min(_CT(LocalCT)['CTPrim'], _CT(Remote1CT)['CTPrim']
																				, _CT(Remote2CT)['CTPrim'])
	if ends == 'OFF':
		return {'Phase Diff': 'Disabled'}
		
	k1 = 20
	Is2 = 2
	Is1 = 0.2
	
	if nF > 0:
		Icharging = 2 * math.pi * (1000 * kV/math.sqrt(3)) * freq * nF * 10**-9
		Is1 = max(2 * Icharging / _CT(LocalCT)['CTPrim'], 0.2)
		Is1 = _myround(Is1, 0.05)

			
	Local = { 'k1': k1 
		 , 'k2': k2
		 , 'Is1': Is1 * _CT(LocalCT)['CTSec']
		 , 'Is2': Is2 * _CT(LocalCT)['CTSec']
		 , 'CT Correction': _myround(_CT(LocalCT)['CTPrim']/CTBase, 0.01)
		}
	Remote1 = { 'k1': k1 
		   , 'k2': k2
		   , 'Is1': Is1 * _CT(Remote1CT)['CTSec']
		   , 'Is2': Is2 * _CT(Remote1CT)['CTSec']
		   , 'CT Correction': _myround(_CT(Remote1CT)['CTPrim']/CTBase, 0.01)
		  }
	result = {'Local': Local,'Remote1': Remote1}						

	if ends==3:
		Remote2 = { 'k1': k1 
			   , 'k2': k2
			   , 'Is1': Is1 * _CT(Remote2CT)['CTSec']
			   , 'Is2': Is2 * _CT(Remote2CT)['CTSec']
			   , 'CT Correction': _myround(_CT(Remote2CT)['CTPrim']/CTBase, 0.01)
			  } 
		result['Remote2'] = Remote2
			
	return result
