"""Module Docstring"""

def vanwarrington(Ifault, length=1):
    """Calculates the resistance of an arc given a fault current and length
Inputs: 
    Ifault = Fault current in Amperes
    length = are length in meters

Output:
    Resistance in ohms to two decimal places"""
    
    Resistance = round(28710 * length / Ifault**1.4, 2)
    return Resistance

def testmodule(n):
    n += 1
    return n
