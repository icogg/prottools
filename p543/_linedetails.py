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
