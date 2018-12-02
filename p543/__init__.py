
import cmath
import math
			
def ct_perf(CT=[1,1], IFault=[], polar=True,ends = 2,**kwargs):
	"""The inputs for the function are:
		
		CT: 	The CT ratio entered as [prim,sec] in amperes. The acutal values used 
			are calculated using the maximum (CT Primary) and minimum (CT Secondary)
	 
		IFault:	The primary in amperes current that is used to determine the CT 
			performance. The values entered are [Magunitude, Angle] unless the switch
			olar is set to False. When set False the input is [Real, Imaginary]
		polar:	(Default = True), when True the current input is in polar
		
		Class:	The class of the CT being assesed, select from 2.5P, 5P, 10P or PX
		
		ALF:	The accuracy limit factor of the given CT (Default is 20)
		
		Vcomp:	The compliance voltage of the CT when specified in accordance with
			AS1675. Either the Vcomp or the Rated Burden must be specified. Where
			both are specified the compliance voltage is used.
						
		RatedBurden: 	The name plate burden in VA for class P CTs. This value is
				not required for class X CTs or those with a compliance voltage 
				pecified.
								
		ActualBurden:	Optional, the actual burden in VA connected to the CT 
				terminals. When not specified the Actual Burden is assumed to be the 
				same as the rated burden. 
									
		Ek:		The Vk or Ek specified by the vendor in volts. This value is only used 
				for class X CTs. 
		
		Rct: 	The internal resistance of the CT in ohms. Use 'estimate' for 
			25mOhms/turn --> 5A CTs
			100mOhms / Turn --?> 1A CTs
					
		Rburden:	The burden of the relays and wiring conneted to the CT terminals.
				Rburden is only used for class X CTs and is specified in Ohms. 
							
		ends: 	(default = 2) The number of terminals being used"""
							
	if len(IFault) == 2:
		if polar:
			IFault = cmath.rect(IFault[0],math.radians(IFault[1]))
		else:
			Ifault = complex(IFault[0], IFault[1])
		XonR = IFault[1] / IFault[0]
	elif len(IFault) == 1:
		IFault = cmath.rect(IFault[0],0)
	else:
		return print('Fault current required')
				
	if len(CT) == 2:
		CTPrim = max(CT)
		CTSec = min(CT)
		CTRatio = CTPrim / CTSec
	else:
		return print('CT Ratio required')
			
	if Rct == 'estimate':
		if CTSec == 5:
			Rct = 0.025 * CTRatio
		else:
			Rct = 0.1 * CTRatio
	
	if Class in ['10P']:
		return print('CT class not recommended')
	
	if Class in ['2.5P', '5P']:
		if Vcomp in locals():
			Ek = Vcomp + (Rct * ALF * CTSec)
		elif RatedBurden in locals():
			Ek = (RatedBurden * ALF) / CTSec + (Rct * ALF * CTSec)
	
	K = Ek / (CTSec * (Rct + Rburden))
	
	Ipu = abs(Ifault) / CTPrim
	
	if ends == 2:
		if (Ipu * XonR) < 1600:
			if K >= max(40 + (0.07 * Ipu * XonR), 107):
				Result = 'OK'
			else:
				Result = 'CT requirements not met'
		
		if (Ipu * XonR) <= 1000:
			if K >= max(40 + (0.07 * Ipu * XonR), 65):
				Result = 'OK'
			else:
				Result = 'CT requirements not met'
		
	if ends == 3:
		if (Ipu * XonR) < 1600:
			if K >= max(40 + (0.35 * Ipu * XonR), 256):
				Result = 'OK'
			else:
				Result = 'CT requirements not met'
		
		if (Ipu * XonR) <= 600:
			if K >= max(40 + (0.35 * Ipu * XonR), 65):
				Result = 'OK'
			else:
				Result = 'CT requirements not met'
	
		if (Ipu * XonR) >= 1600:
			Result = 'CT requirements not met'
			
	return print(Result)


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
