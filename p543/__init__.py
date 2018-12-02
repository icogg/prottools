
import cmath
import math
			
def _CT(CT=[]):
	"""Input a list containing [CTPrimary, CTSecondary]. The return is a 
	 dictionary with primary, secondary and ratio"""
	if len(CT) == 2:
		CTPrim = max(CT)
		CTSec = min(CT)
		CTRatio = CTPrim / CTSec
	else:
		return print('CT Ratio required')
	return{'CTPrim':CTPrim
	       , 'CTSec':CTSec
	       , 'CTRatio':CTRatio
	      }

def _myround(x, base=5):
	return base * round(float(x) / base)
	

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

def line_details(Z1_polar=True, Z1=[]
                 , Z0_polar=True, Z0=[]
                 , length=1
                 , CT=[1,1], VT=[1,1]
                 , Prim=True):
    """This function returns the line details for a MiCOM P543 relay
    Inputs:
        Z1_polar: Set True if the input values for the line positive sequence impedance is in polar
                  Set False for rectangular coordinates
        Z1: [Z1mag, Z1ang] for Z1_Polar = True, [R , jX] for Z1_Polar = False
        
        Z0_polar: Set True if the input values for the line positive sequence impedance is in polar
                  Set False for rectangular coordinates
        Z0: [Z0mag, Z0ang] for Z0_Polar = True, [R , jX] for Z0_Polar = False
        
        CT: [Primary, Secondary]
        VT: [Primary, Secondary]
        
        Prim: Set True when the input parameters are in primary values, Set False for Secondary Values
    
    Outputs:
        A dictionary containing the following variables (in secondary values)
        Z1mag:
        Z1ang:
        K0mag:
        K0ang:
    
    """
    
    if len(Z1) != 2:
        print('Z1 Argument Error')
        return
    
    if len(Z0) != 2:
        print('Z0 Argument Error')
        return
    
    
    if Z1_polar:
        Z1 = cmath.rect(Z1[0],math.radians(Z1[1]))
    else:
        Z1 = complex(Z1[0],Z1[1])

    if Z0_polar:
        Z0 = cmath.rect(Z0[0],math.radians(Z0[1]))
    else:
        Z0 = complex(Z0[0],Z0[1])
        
    
    if Prim:
        CTR = max(CT) / min(CT)
        VTR = max(VT) / min(VT)
        Z0 = Z0 * CTR/VTR
        Z1 = Z1 * CTR/VTR
    
    K0 = (Z0-Z1)/(3*Z1)
    
    K0mag = round(abs(K0),2)
    K0ang = round(math.degrees(cmath.phase(K0)),0)

    Z1mag = round(abs(Z1),2)
    Z1ang = round(math.degrees(cmath.phase(Z1)),0)

 
    return {'Z1mag':Z1mag, 'Z1ang':Z1ang, 'K0mag':K0mag, 'K0ang':K0ang}
