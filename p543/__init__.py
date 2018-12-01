
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
		return print(CTR)
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
