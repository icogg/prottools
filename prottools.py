"""Module Docstring"""

def vanwarrington(Ifault, length=1):
    """Calculates the resistance of an arc given a fault current and length
Inputs: 
    Ifault = Fault current in Amperes
    length = are length in meters

Output:
    Resistance in ohms"""
    
    Resistance = 28710 * length / Ifault**1.4    
    return Resistance
