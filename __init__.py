def vanwarrington(Ifault, length=1):
    """Calculates the resistance of an arc given a fault current and length
Inputs: 
    Ifault = Fault current in Amperes
    length = are length in meters

Output:
    Resistance in ohms to two decimal places"""
    
    Resistance = round(28710 * length / Ifault**1.4, 2)
    return Resistance


def apparentimpedance(polar=True
                  , Vrelay = []
                  , PhaseCurrent = []
                  , ResidualCurrent=[]
                  , kZ0 =[]
                  , CT=[1,1]
                  , VT=[1,1]
                  , Prim=True
                 , Ground=False):
    """This function returns the ********* for a MiCOM P543 relay
    Inputs:

        
        CT: [Primary, Secondary]
        VT: [Primary, Secondary]
        
        Prim: Set True when the input parameters are in primary values, Set False for Secondary Values
    
    Outputs:
        A dictionary containing the following variables (in secondary values)
        Zmag:
        Zang:
    
    """

    if len(Vrelay) != 2:
        print('Argument Error')
        return
    
    if len(PhaseCurrent) != 2:
        print('Argument Error')
        return 

    if polar:
        Voltage = cmath.rect(Vrelay[0],math.radians(Vrelay[1]))
        PhaseCurrent = cmath.rect(PhaseCurrent[0],math.radians(PhaseCurrent[1]))
    else:
        Voltage = complex(Vrelay[0],Vrelay[1])
        PhaseCurrent = complex(PhaseCurrent[0],PhaseCurrent[1])    
    
    if Ground:
        if len(ResidualCurrent) != 2:
            print('Argument Error')
            return
        if len(kZ0) != 2:
            print('Argument Error')
            return
        if polar:
            ResidualCurrent = cmath.rect(ResidualCurrent[0],math.radians(ResidualCurrent[1]))
        else:
            ResidualCurrent = complex(ResidualCurrent[0],ResidualCurrent[1])
        
        kZ0 = cmath.rect(kZ0[0],math.radians(kZ0[1]))
        
        Z = Voltage / (PhaseCurrent + ResidualCurrent*kZ0)
    
    else:
        Z = Voltage / PhaseCurrent
   
    if Prim:
        CTR = max(CT) / min(CT)
        VTR = max(VT) / min(VT)
        Z = Z * CTR/VTR
    
    Zmag = round(abs(Z),3)
    Zang = round(math.degrees(cmath.phase(Z)),0)
    
    
    return {'Zmag':Zmag, 'Zang':Zang}
