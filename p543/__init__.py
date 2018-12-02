import cmath
import math
from .currenttransfomer import *
from .linediff import *

			
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
	
