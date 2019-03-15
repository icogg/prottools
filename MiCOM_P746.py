# from IPython.display import Image


class MiCOM_P746(object):
    def __init__(self,
                 PlantReference='<SUB><BAY><DEV>',
                 Description='Example',
                 CTs=[],
                 PTOCs=[],
                 Ifault3ph=10000,
                 IfaultSLG=10000):

        self.PlantReference = PlantReference
        self.Description = Description
        self.CTs = CTs
        self.ABCPhaseRotation = True
        self.Zone1 = []
        self.Zone2 = []
        self.ChZone = []
        self.Ifault3ph = Ifault3ph
        self.k1 = 10
        self.k2 = 65
        self.kCZ = 30
        self.tDiff = 0
        self.PTOCs = PTOCs

    @property
    def BB12Coupling(self):
        return self._BB12Coupling

    @BB12Coupling.setter
    def BB12Coupling(self, value):

        settinglist = [
            'None', 'Breaker Only', 'Isolator Only', 'Breaker&Isolator'
        ]
        if value not in settinglist:
            raise ValueError('Setting needs to be from: %s' %
                             (', '.join(settinglist)))
        self._BB12Coupling = {
            'Setting': '303F',
            'Description': 'BB12 Coupling by',
            'Value': value
        }

    @property
    def BB12BB1CTPolarity(self):
        return self._BB12BB1CTPolarity

    @BB12BB1CTPolarity.setter
    def BB12BB1CTPolarity(self, value):
        settinglist = ['Standard', 'Inverted']
        if value not in settinglist:
            raise ValueError('Setting needs to be from: %s' %
                             (', '.join(settinglist)))
        self._BB12BB1CTPolarity = {
            'Setting': '3041',
            'Description': 'BB12:BB1 CT Pol',
            'Value': value
        }

    @property
    def BB12BB2CTPolarity(self):
        return self._BB12BB2CTPolarity

    @BB12BB2CTPolarity.setter
    def BB12BB2CTPolarity(self, value):
        settinglist = ['Standard', 'Inverted']
        if value not in settinglist:
            raise ValueError('Setting needs to be from: %s' %
                             (', '.join(settinglist)))
        self._BB12BB2CTPolarity = {
            'Setting': '3043',
            'Description': 'BB12:BB2 CT Pol',
            'Value': value
        }

    @property
    def BB12BusCTBB1(self):
        return self._BB12BusCTBB1

    @BB12BusCTBB1.setter
    def BB12BusCTBB1(self, value):
        if value not in ['NO CT', 'CT1']:
            raise ValueError('Entry must be either NO CT or CT1')
        self._BB12BusCTBB1 = {
            'Setting': '3040',
            'Description': 'BB12 Bus CT/BB1',
            'Value': value
        }

    @property
    def BB12BusCTBB2(self):
        return self._BB12BusCTBB2

    @BB12BusCTBB2.setter
    def BB12BusCTBB2(self, value):
        if value not in ['NO CT', 'CT1']:
            raise ValueError('Entry must be either NO CT or CT1')
        self._BB12BusCTBB2 = {
            'Setting': '3042',
            'Description': 'BB12 Bus CT/BB2',
            'Value': value
        }

    def configureCoupler(self,
                         CTLocation='Bus1',
                         PolarityBus1=True,
                         Equipment='None'):
        if CTLocation not in ['Bus1', 'Bus2', 'Not Fitted']:
            raise ValueError('CT location must be either Bus1 or Bus2')

        equipmentlist = [
            'None', 'Breaker Only', 'Isolator Only', 'Breaker&Isolator'
        ]

        if Equipment not in equipmentlist:
            raise ValueError('Setting needs to be from: %s' %
                             (', '.join(settinglist)))

        if CTLocation == 'Bus1':
            self.BB12BusCTBB1 = 'CT1'
            self.BB12BusCTBB2 = 'NO CT'
        elif CTLocation == 'Bus2':
            self.BB12BusCTBB1 = 'NO CT'
            self.BB12BusCTBB2 = 'CT1'
        else:
            self.BB12BusCTBB1 = 'NO CT'
            self.BB12BusCTBB2 = 'NO CT'
        if PolarityBus1:
            self.BB12BB1CTPolarity = 'Standard'
            self.BB12BB2CTPolarity = 'Inverted'
        else:
            self.BB12BB1CTPolarity = 'Inverted'
            self.BB12BB2CTPolarity = 'Standard'
        if Equipment == 'None':
            print('No Modification to PSL Required')
        elif Equipment == 'Breaker Only':
            print('Map Bus Tie - Breaker Only No CT in PSL')
        elif Equipment == 'Isolator Only':
            print('Map Bus Tie - Isolator Only in PSL')
        else:
            if CTLocation == 'Not Fitted':
                print('Map Bus Tie - Breaker & Isolator No CT in PSL')
        self.BB12Coupling = Equipment

    @property
    def Ifault3ph(self):
        return self._Ifault3ph

    @Ifault3ph.setter
    def Ifault3ph(self, value):
        if not isinstance(value, (float, int)):
            raise ValueError('Please enter a number')
        self._Ifault3ph = value

    @property
    def IfaultSLG(self):
        return self._IfaultSLG

    @IfaultSLG.setter
    def IfaultSLG(self, value):
        if not isinstance(value, (float, int)):
            raise ValueError('Please enter a number')
        self._IfaultSLG = value

    @property
    def PlantReference(self):
        return self._PlantReference

    @PlantReference.setter
    def PlantReference(self, value):
        if len(value) > 16:
            raise ValueError('Text Length too long')
        self._PlantReference = {
            'Setting': '0005',
            'Description': 'Plant Reference',
            'Value': value.upper()
        }

    @property
    def Description(self):
        return self._Description

    @Description.setter
    def Description(self, value):
        if len(value) > 16:
            raise ValueError('Text Length too long')
        self._Description = {
            'Setting': '0004',
            'Description': 'Description',
            'Value': value.upper()
        }

    @property
    def SubstationDCVoltage(self):
        return self._SubstationDCVoltage

    @SubstationDCVoltage.setter
    def SubstationDCVoltage(self, value):
        if not isinstance(value, (float, int)):
            raise ValueError('Please enter a number')
        if value >= 220:
            DC = '220/250V'
        elif value >= 110:
            DC = '110/125V'
        elif value >= 48:
            DC = '48/54V'
        else:
            DC = '24/27V'
        self._SubstationDCVoltage = {
            'Setting': '1101',
            'Description': 'Global Nominal V',
            'Value': DC
        }

    @property
    def ABCPhaseRotation(self):
        return self._ABCPhaseRotation

    @ABCPhaseRotation.setter
    def ABCPhaseRotation(self, value):
        if value:
            Sequence = 'Standard ABC'
        else:
            Sequence = 'Reverse ACB'
        self._ABCPhaseRotation = {
            'Setting': '3032',
            'Description': 'Phase Sequence',
            'Value': Sequence
        }

    @property
    def Zone1(self):
        return self._Zone1

    @Zone1.setter
    def Zone1(self, value):
        if not all(isinstance(item, int) for item in value):
            raise ValueError('Entries must be integers')

        if not all(item >= 1 for item in value):
            raise ValueError('Entries must be in range 1 to 7')

        if not all(item <= 7 for item in value):
            raise ValueError('Entries must be in range 1 to 7')

        unique = []
        [unique.append(item) for item in value if item not in unique]

        Zone = '{:08b}'.format(sum([2**(x - 1) for x in value]))
        self._Zone1 = {
            'Setting': '3035',
            'Description': 'BB1 Terminals',
            'Value': Zone
        }

    @property
    def Zone2(self):
        return self._Zone2

    @Zone2.setter
    def Zone2(self, value):
        if not all(isinstance(item, int) for item in value):
            raise ValueError('Entries must be integers')

        if not all(item >= 1 for item in value):
            raise ValueError('Entries must be in range 1 to 7')

        if not all(item <= 7 for item in value):
            raise ValueError('Entries must be in range 1 to 7')

        unique = []
        [unique.append(item) for item in value if item not in unique]

        Zone = '{:08b}'.format(sum([2**(x - 1) for x in unique]))
        self._Zone2 = {
            'Setting': '3036',
            'Description': 'BB2 Terminals',
            'Value': Zone
        }

    @property
    def ChZone(self):
        return self._ChZone

    @ChZone.setter
    def ChZone(self, value):
        if not all(isinstance(item, int) for item in value):
            raise ValueError('Entries must be integers')

        if not all(item >= 1 for item in value):
            raise ValueError('Entries must be in range 1 to 7')

        if not all(item <= 7 for item in value):
            raise ValueError('Entries must be in range 1 to 7')

        unique = []
        [unique.append(item) for item in value if item not in unique]

        Zone = '{:08b}'.format(sum([2**(x - 1) for x in value]))
        self._ChZone = {
            'Setting': '3039',
            'Description': 'ChZONE Terminal',
            'Value': Zone
        }

    def setcheckzone(self):
        TempZone = []
        Z1 = int(self.Zone1['Value'][-7:], 2)
        Z2 = int(self.Zone2['Value'][-7:], 2)

        usedterminals = Z1 | Z2
        uniqueterminals = 0b1111111 - (Z1 & Z2)
        checkterminals = (usedterminals & uniqueterminals)

        for idx, char in enumerate(reversed('{:08b}'.format(checkterminals))):
            if char == '1':
                TempZone.append(idx + 1)
        self.ChZone = TempZone

    @property
    def NumberofFeeders(self):
        return self._NumberofFeeders

    @NumberofFeeders.setter
    def NumberofFeeders(self, value):
        if not isinstance(value, int):
            raise ValueError('Entry must be an integer')

        if not value >= 0:
            raise ValueError('Entry must be in range 0 to 7')

        if not value <= 7:
            raise ValueError('Entry must be in range 0 to 7')

        self._NumberofFeeders = {
            'Setting': '3033',
            'Description': 'Feeder Numbers',
            'Value': value
        }

    @property
    def tDiff(self):
        return self._tDiff

    @tDiff.setter
    def tDiff(self, value):
        if not isinstance(value, (float, int)):
            raise ValueError('Entries must be a number')

        if not value >= 0:
            raise ValueError('Entries must be in range 0 to 10 seconds')

        if not value <= 10:
            raise ValueError('Entries must be in range 0 to 10 seconds')

        self._tDiff = {
            'Setting': '3107',
            'Description': 'tDIFF',
            'Value': value
        }

    @property
    def ID1(self):
        return self._ID1

    @ID1.setter
    def ID1(self, value):
        if not isinstance(value, (float, int)):
            raise ValueError('Entries must be a number')

        if not value >= 0.025:
            raise ValueError('Entries must be in range 0.025 to 2.5')

        if not value <= 2.5:
            raise ValueError('Entries must be in range 0.025 to 2.5')

        self._ID1 = {
            'Setting': '3141',
            'Description': 'ID>1 Current',
            'Value': value
        }

    def setID1(self, pcnt=2):
        value = 0
        for ct in self.CTs:
            if (ct.Primary['Value'] * pcnt / 100) > value:
                value = (ct.Primary['Value'] * pcnt / 100)
        Iset = max(value, 50)
        self.ID1 = Iset / 2000
        print('Supervision Pickup set to {:6.2f} A primary'.format(Iset))

    @property
    def ID2(self):
        return self._ID2

    @ID2.setter
    def ID2(self, value):
        if not isinstance(value, (float, int)):
            raise ValueError('Entries must be a number')

        if not value >= 0.025:
            raise ValueError('Entries must be in range 0.025 to 50')

        if not value <= 50:
            raise ValueError('Entries must be in range 0.025 to 50')

        self._ID2 = {
            'Setting': '3103',
            'Description': 'ID>2 Current',
            'Value': value
        }

    def setID2(self, IfMin):
        if not isinstance(IfMin, (float, int)):
            raise ValueError('IfMin must be a number')
        IloadMax = 0
        for ct in self.CTs:
            if ct.Iload > IloadMax:
                IloadMax = ct.Iload

        Iset = min(1.2 * IloadMax, 0.8 * IfMin)

        if not Iset >= (1.2 * IloadMax):
            raise ValueError('Setting below 120% load, check load currents')
        if not Iset <= (0.8 * IfMin):
            raise ValueError(
                'Setting above 80% Ifmin, check load currents or set pickup manually'
            )

        print('Diff Pickup set to {:6.2f} A primary'.format(Iset))

        self.ID2 = max(Iset, 50) / 2000

    @property
    def IDCZ2(self):
        return self._IDCZ2

    @IDCZ2.setter
    def IDCZ2(self, value):
        if not isinstance(value, (float, int)):
            raise ValueError('Entries must be a number')

        if not value >= 0.025:
            raise ValueError('Entries must be in range 0.025 to 50')

        if not value <= 50:
            raise ValueError('Entries must be in range 0.025 to 50')

        self._IDCZ2 = {
            'Setting': '3113',
            'Description': 'IDCZ>2 Current',
            'Value': value
        }

    def setIDCZ2(self):
        self.IDCZ2 = self.ID2['Value']
        print('CheckZone Pickup set to the same as ID>2')

    @property
    def k1(self):
        return self._k1

    @k1.setter
    def k1(self, pcnt=10):
        if not isinstance(pcnt, (int)):
            raise ValueError('Entries must be an integer')

        if not pcnt >= 0:
            raise ValueError('Entries must be in range 0 to 50')

        if not pcnt <= 50:
            raise ValueError('Entries must be in range 0 to 50')

        self._k1 = {
            'Setting': '3142',
            'Description': 'Slope k1',
            'Value': pcnt
        }

    @property
    def k2(self):
        return self._k2

    @k2.setter
    def k2(self, pcnt=65):
        if not isinstance(pcnt, (int)):
            raise ValueError('Entries must be an integer')

        if not pcnt >= 20:
            raise ValueError('Entries must be in range 20 to 90')

        if not pcnt <= 90:
            raise ValueError('Entries must be in range 20 to 90')

        self._k2 = {
            'Setting': '3104',
            'Description': 'Slope k2',
            'Value': pcnt
        }

    @property
    def kCZ(self):
        return self._kCZ

    @kCZ.setter
    def kCZ(self, pcnt=30):
        if not isinstance(pcnt, (int)):
            raise ValueError('Entries must be an integer')

        if not pcnt >= 0:
            raise ValueError('Entries must be in range 0 to 90')

        if not pcnt <= 90:
            raise ValueError('Entries must be in range 0 to 90')

        self._kCZ = {
            'Setting': '3114',
            'Description': 'Slope kCZ',
            'Value': pcnt
        }

    def setnumberoffeeders(self):
        # is this the number of inputs including the bus section
        Z1 = int(self.Zone1['Value'][-7:], 2)
        Z2 = int(self.Zone2['Value'][-7:], 2)

        usedterminals = Z1 | Z2
        uniqueterminals = 0b1111111 - (Z1 & Z2)
        checkterminals = (usedterminals & uniqueterminals)

        terminals = 0

        for idx, bit in enumerate('{:08b}'.format(checkterminals)):
            if bit == '1':
                terminals += 1

        self.NumberofFeeders = terminals

    @property
    def NumberofBusbars(self):
        return self._NumberofBusbars

    @NumberofBusbars.setter
    def NumberofBusbars(self, value):
        if not isinstance(value, int):
            raise ValueError('Entry must be an integer')

        if not value >= 0:
            raise ValueError('Entry must be in range 0 to 2')

        if not value <= 7:
            raise ValueError('Entry must be in range 0 to 2')

        self._NumberofBusbars = {
            'Setting': '3034',
            'Description': 'Busbar Numbers',
            'Value': value
        }

    def setnumberofbusbars(self):
        # is this the number of inputs including the bus section
        Busbars = 0
        Z1 = int(self.Zone1['Value'][-7:], 2)
        Z2 = int(self.Zone2['Value'][-7:], 2)

        if Z1 > 0:
            Busbars += 1
        if Z2 > 0:
            Busbars += 1

        self.NumberofBusbars = Busbars

    @property
    def PhCompPURatio(self):
        return self._PhCompPURatio

    @PhCompPURatio.setter
    def PhCompPURatio(self, pcnt=10):
        if not isinstance(pcnt, (int)):
            raise ValueError('Entries must be an integer')
        if not pcnt >= 5:
            raise ValueError('Entries must be in range 5 to 250')
        if not pcnt <= 250:
            raise ValueError('Entries must be in range 5 to 250')
        self._PhCompPURatio = {
            'Setting': '3170',
            'Description': 'PhComp PU Ratio',
            'Value': pcnt
        }

    def checkCT(self, Ifault, Terminal=None):
        CTResults = []
        for ct in self.CTs:
            FaultRatio = Ifault / (ct.Primary['Value'] * 20)
            LoadRatio = ct.Iload / ct.Primary['Value']
            KneePointRatio = ((Ifault / ct.Primary['Value']) *
                              (ct.loop_resistance + ct.Rct)) / ct.Ek

            if Terminal is None:
                Termlist = [1, 2, 3, 4, 5, 6, 7]
            else:
                Termlist = Terminal

            if ct.Terminal in Termlist:
                CTResults.append({
                    'Fault Ratio': FaultRatio,
                    'Load Ratio': LoadRatio,
                    'Kneepoint Ratio': KneePointRatio
                })
                if LoadRatio > 1:
                    print('Terminal {} load current above rating'.format(
                        ct.Terminal))
                elif FaultRatio > 1:
                    print('Terminal {} fault current above 20 times rating'.
                          format(ct.Terminal))
                elif KneePointRatio > 1:
                    print('Terminal {} Ek inadequate'.format(ct.Terminal))
                else:
                    print('Terminal {} CT Suitable'.format(ct.Terminal))

        for result in CTResults:
            print(result)

    def createCT(self, CT):
        # delete the CT if is already in the CT list, then add the record

        try:
            for ix, ct in enumerate(self.CTs):
                if ct.Terminal == CT.Terminal:
                    del self.CTs[ix]
        except:
            pass
        self.CTs.append(CT)

    def showCT(self):
        if len(self.CTs) > 0:
            variables = self.CTs[0].__dict__.keys()
            for v in variables:
                print(v)
            # print(variables)
            for CT in self.CTs:
                pass
        else:
            return print('No CTs added to the scheme')

    def lenCT(self):
        return len(self.CTs)

    def createPTOC(self, PTOC):
        # delete the PTOC if is already in the CT list, then add the record

        try:
            for ix, ptoc in enumerate(self.PTOCs):
                if ptoc.Terminal == PTOC.Terminal:
                    if ptoc.Type == PTOC.Type:
                        del self.PTOCs[ix]
        except:
            pass

        self.PTOCs.append(PTOC)


class CT(object):
    """This class is used to store a current transfomer bank and provide the
    calculations to support the CT
    """

    def __init__(self,
                 Terminal=None,
                 Primary=800,
                 Secondary=1,
                 Polarity='Standard',
                 Type='PX',
                 Rct=1.2,
                 Length=100,
                 Ek=600,
                 WireSize=4):
        self.Terminal = Terminal
        self.Primary = Primary
        self.Secondary = Secondary
        self.Polarity = Polarity
        self.Type = Type
        self.Rct = Rct
        self.Length = Length
        self.Ek = Ek
        self.WireSize = WireSize
        self.loop_resistance = self.loop_res()
        self.Iload = Primary

    @property
    def Terminal(self):
        return self._Terminal

    @Terminal.setter
    def Terminal(self, value):
        if not isinstance(value, int):
            raise ValueError('Entry must be an integer')

        if not value >= 1:
            raise ValueError('Entry must be in range 1 to 7')

        if not value <= 7:
            raise ValueError('Entry must be in range 1 to 7')

        self._Terminal = value

    @property
    def Primary(self):
        return self._Primary

    @Primary.setter
    def Primary(self, value):
        if not isinstance(value, int):
            raise ValueError('Entry must be an integer')

        if not value >= 1:
            raise ValueError('Entry must be in range 1 to 30000')

        if not value <= 30000:
            raise ValueError('Entry must be in range 1 to 30000')

        if self.Terminal == 1:
            self._Primary = {
                'Setting': '0A12',
                'Description': 'T1 CT Primary',
                'Value': value
            }
        elif self.Terminal == 2:
            self._Primary = {
                'Setting': '0A16',
                'Description': 'T2 CT Primary',
                'Value': value
            }
        elif self.Terminal == 3:
            self._Primary = {
                'Setting': '0A1A',
                'Description': 'T3 CT Primary',
                'Value': value
            }
        elif self.Terminal == 4:
            self._Primary = {
                'Setting': '0A1E',
                'Description': 'T4 CT Primary',
                'Value': value
            }
        elif self.Terminal == 5:
            self._Primary = {
                'Setting': '0A22',
                'Description': 'T5 CT Primary',
                'Value': value
            }
        elif self.Terminal == 6:
            self._Primary = {
                'Setting': '0A26',
                'Description': 'T6 CT Primary',
                'Value': value
            }
        else:
            self._Primary = {
                'Setting': '0A2A',
                'Description': 'T7 CT Primary',
                'Value': value
            }

    @property
    def Secondary(self):
        return self._Secondary

    @Secondary.setter
    def Secondary(self, value):
        if not isinstance(value, int):
            raise ValueError('Entry must be an integer')

        if value not in [1, 5]:
            raise ValueError('Entry must be either 1 or 5')

        if self.Terminal == 1:
            self._Secondary = {
                'Setting': '0A13',
                'Description': 'T1 CT Secondary',
                'Value': value
            }
        elif self.Terminal == 2:
            self._Secondary = {
                'Setting': '0A17',
                'Description': 'T2 CT Secondary',
                'Value': value
            }
        elif self.Terminal == 3:
            self._Secondary = {
                'Setting': '0A1B',
                'Description': 'T3 CT Secondary',
                'Value': value
            }
        elif self.Terminal == 4:
            self._Secondary = {
                'Setting': '0A1F',
                'Description': 'T4 CT Secondary',
                'Value': value
            }
        elif self.Terminal == 5:
            self._Secondary = {
                'Setting': '0A23',
                'Description': 'T5 CT Secondary',
                'Value': value
            }
        elif self.Terminal == 6:
            self._Secondary = {
                'Setting': '0A27',
                'Description': 'T6 CT Secondary',
                'Value': value
            }
        else:
            self._Secondary = {
                'Setting': '0A2B',
                'Description': 'T7 CT Secondary',
                'Value': value
            }

    @property
    def Polarity(self):
        return self._Polarity

    @Polarity.setter
    def Polarity(self, value):
        if value not in ['Standard', 'Inverted']:
            raise ValueError('Entry must be either Standard or Inverted')

        if self.Terminal == 1:
            self._Polarity = {
                'Setting': '0A11',
                'Description': 'T1 CT Polarity',
                'Value': value
            }
        elif self.Terminal == 2:
            self._Polarity = {
                'Setting': '0A15',
                'Description': 'T2 CT Polarity',
                'Value': value
            }
        elif self.Terminal == 3:
            self._Polarity = {
                'Setting': '0A19',
                'Description': 'T3 CT Polarity',
                'Value': value
            }
        elif self.Terminal == 4:
            self._Polarity = {
                'Setting': '0A1D',
                'Description': 'T4 CT Polarity',
                'Value': value
            }
        elif self.Terminal == 5:
            self._Polarity = {
                'Setting': '0A21',
                'Description': 'T5 CT Polarity',
                'Value': value
            }
        elif self.Terminal == 6:
            self._Polarity = {
                'Setting': '0A25',
                'Description': 'T6 CT Polarity',
                'Value': value
            }
        else:
            self._Polarity = {
                'Setting': '0A29',
                'Description': 'T7 CT Polarity',
                'Value': value
            }

    @property
    def Iload(self):
        return self._Iload

    @Iload.setter
    def Iload(self, value):
        if not isinstance(value, (float, int)):
            raise ValueError('Please enter a number')
        self._Iload = value

    @property
    def Type(self):
        return self._Type

    @Type.setter
    def Type(self, value):
        if value not in ['PX', '2.5P', '5P']:
            raise ValueError('Class needs to be PX, 2.5P, 5P')
        self._Type = value

    @property
    def Length(self):
        return self._Length

    @Length.setter
    def Length(self, value):
        if not isinstance(value, (float, int)):
            raise ValueError('Please enter a number')
        self._Length = value

    @property
    def Ek(self):
        return self._Ek

    @Ek.setter
    def Ek(self, value):
        if not isinstance(value, (float, int)):
            raise ValueError('Please enter a number')
        self._Ek = value

    @property
    def Rct(self):
        return self._Rct

    @Rct.setter
    def Rct(self, value):
        if not isinstance(value, (float, int)):
            raise ValueError('Please enter a number')
        self._Rct = value

    @property
    def WireSize(self):
        return self._WireSize

    @WireSize.setter
    def WireSize(self, value):
        if value not in [2.5, 4, 6, 10]:
            raise ValueError('Entry must either 2.5, 4, 6, 10')
        self._WireSize = value

    def loop_res(self):
        if self.Secondary == 5:
            Rrelay = 0.04
        else:
            Rrelay = 0.008

        if self.WireSize == 2.5:
            return self.Length * (7.6 / 1000) + Rrelay
        if self.WireSize == 4:
            return self.Length * (4.52 / 1000) + Rrelay
        if self.WireSize == 6:
            return self.Length * (3.02 / 1000) + Rrelay
        if self.WireSize == 10:
            return self.Length * (1.79 / 1000) + Rrelay
        if type(self.WireSize) == type(str):
            try:
                float(self.WireSize)
            except:
                print('Invalid custom loop resistance')


class PTOC(object):
    """This class is used to store an overcurrent setting
	"""

    def __init__(self,
                 CTPrimary=1,
                 CTSecondary=1,
                 Terminal=None,
                 Type='OC',
                 IDMTPickup='Disabled',
                 HighsetPickup='Disabled',
                 Curve='Disabled',
                 TMS=0.1):
        self.Terminal = Terminal
        self.Type = Type
        self.CTPrimary = CTPrimary
        self.CTSecondary = CTSecondary
        self.Curve = Curve
        self.IDMTPickup = IDMTPickup
        self.TMS = TMS
        self.tReset = 0
        self.HighsetPickup = HighsetPickup
        self.HighsetDelay = 0

    @property
    def Type(self):
        return self._Type

    @Type.setter
    def Type(self, value):
        if value not in ['OC', 'EF']:
            raise ValueError('Entry must be either OC or EF')
        self._Type = value

    @property
    def Terminal(self):
        return self._Terminal

    @Terminal.setter
    def Terminal(self, value):
        if not isinstance(value, int):
            raise ValueError('Entry must be an integer')
        if not value >= 1:
            raise ValueError('Entry must be in range 1 to 7')
        if not value <= 7:
            raise ValueError('Entry must be in range 1 to 7')
        self._Terminal = value

    @property
    def Curve(self):
        return self._Curve

    @Curve.setter
    def Curve(self, value):
        _curvelist = [
            'Disabled', 'DT', 'IEC S Inverse', 'IEC V Inverse',
            'IEC E Inverse', 'UK LT Inverse'
            'UK Rectifier', 'RI', 'IEEE M Inverse', 'IEEE V Inverse',
            'IEEE E Inverse', 'US Inverse', 'US ST Inverse'
        ]

        if value not in _curvelist:
            raise ValueError('Please enter a curve from ' +
                             ' '.join(_curvelist))
        if self.Terminal == 1:
            if self.Type == 'OC':
                self._Curve = {
                    'Setting': '3502',
                    'Description': 'T1 I>1 Function',
                    'Value': value
                }
            else:
                self._Curve = {
                    'Setting': '3803',
                    'Description': 'T1 IN>1 Function',
                    'Value': value
                }
        elif self.Terminal == 2:
            if self.Type == 'OC':
                self._Curve = {
                    'Setting': '3522',
                    'Description': 'T2 I>1 Function',
                    'Value': value
                }
            else:
                self._Curve = {
                    'Setting': '3833',
                    'Description': 'T2 IN>1 Function',
                    'Value': value
                }
        elif self.Terminal == 3:
            if self.Type == 'OC':
                self._Curve = {
                    'Setting': '3542',
                    'Description': 'T3 I>1 Function',
                    'Value': value
                }
            else:
                self._Curve = {
                    'Setting': '3863',
                    'Description': 'T3 IN>1 Function',
                    'Value': value
                }
        elif self.Terminal == 4:
            if self.Type == 'OC':
                self._Curve = {
                    'Setting': '3562',
                    'Description': 'T4 I>1 Function',
                    'Value': value
                }
            else:
                self._Curve = {
                    'Setting': '3891',
                    'Description': 'T4 IN>1 Function',
                    'Value': value
                }
        elif self.Terminal == 5:
            if self.Type == 'OC':
                self._Curve = {
                    'Setting': '3582',
                    'Description': 'T5 I>1 Function',
                    'Value': value
                }
            else:
                self._Curve = {
                    'Setting': '38B1',
                    'Description': 'T5 IN>1 Function',
                    'Value': value
                }
        elif self.Terminal == 6:
            if self.Type == 'OC':
                self._Curve = {
                    'Setting': '35A2',
                    'Description': 'T6 I>1 Function',
                    'Value': value
                }
            else:
                self._Curve = {
                    'Setting': '38D1',
                    'Description': 'T6 IN>1 Function',
                    'Value': value
                }
        else:
            if self.Type == 'OC':
                self._Curve = {
                    'Setting': '35C2',
                    'Description': 'T7 I>1 Function',
                    'Value': value
                }
            else:
                self._Curve = {
                    'Setting': '38F1',
                    'Description': 'T7 IN>1 Function',
                    'Value': value
                }

    @property
    def TMS(self):
        return self._TMS

    @TMS.setter
    def TMS(self, value):
        if not isinstance(value, (float, int)):
            raise ValueError('Please enter a number')
        if not value >= 0.025:
            raise ValueError('Entry must be in range 0.025 to 1.2')
        if not value <= 1.2:
            raise ValueError('Entry must be in range 0.025 to 1.2')

        if self.Terminal == 1:
            if self.Type == 'OC':
                self._TMS = {
                    'Setting': '3506',
                    'Description': 'T1 I>1 TMS',
                    'Value': value
                }
            else:
                self._TMS = {
                    'Setting': '3809',
                    'Description': 'T1 IN>1 TMS',
                    'Value': value
                }

        elif self.Terminal == 2:
            if self.Type == 'OC':
                self._TMS = {
                    'Setting': '3526',
                    'Description': 'T2 I>1 TMS',
                    'Value': value
                }
            else:
                self._TMS = {
                    'Setting': '3839',
                    'Description': 'T2 IN>1 TMS',
                    'Value': value
                }
        elif self.Terminal == 3:
            if self.Type == 'OC':
                self._TMS = {
                    'Setting': '3546',
                    'Description': 'T3 I>1 TMS',
                    'Value': value
                }
            else:
                self._TMS = {
                    'Setting': '3869',
                    'Description': 'T3 IN>1 TMS',
                    'Value': value
                }
        elif self.Terminal == 4:
            if self.Type == 'OC':
                self._TMS = {
                    'Setting': '3566',
                    'Description': 'T4 I>1 TMS',
                    'Value': value
                }
            else:
                self._TMS = {
                    'Setting': '3897',
                    'Description': 'T4 IN>1 TMS',
                    'Value': value
                }
        elif self.Terminal == 5:
            if self.Type == 'OC':
                self._TMS = {
                    'Setting': '3586',
                    'Description': 'T5 I>1 TMS',
                    'Value': value
                }
            else:
                self._TMS = {
                    'Setting': '38B7',
                    'Description': 'T5 IN>1 TMS',
                    'Value': value
                }
        elif self.Terminal == 6:
            if self.Type == 'OC':
                self._TMS = {
                    'Setting': '35A6',
                    'Description': 'T6 I>1 TMS',
                    'Value': value
                }
            else:
                self._TMS = {
                    'Setting': '38F7',
                    'Description': 'T6 IN>1 TMS',
                    'Value': value
                }
        else:
            if self.Type == 'OC':
                self._TMS = {
                    'Setting': '38C6',
                    'Description': 'T7 I>1 TMS',
                    'Value': value
                }
            else:
                self._TMS = {
                    'Setting': '3806',
                    'Description': 'T7 IN>1 TMS',
                    'Value': value
                }

    @property
    def tReset(self):
        return self._tReset

    @tReset.setter
    def tReset(self, value):
        if not isinstance(value, (float, int)):
            raise ValueError('Please enter a number')
        if not value >= 0:
            raise ValueError('Entry must be in range 0 to 100s')
        if not value <= 100:
            raise ValueError('Entry must be in range 0 to 100s')

        if self.Terminal == 1:
            if self.Type == 'OC':
                self._tReset = {
                    'Setting': '350A',
                    'Description': 'T1 I>1 tReset',
                    'Value': value
                }
            else:
                self._tReset = {
                    'Setting': '380F',
                    'Description': 'T1 IN>1 tReset',
                    'Value': value
                }
        elif self.Terminal == 2:
            if self.Type == 'OC':
                self._tReset = {
                    'Setting': '352A',
                    'Description': 'T2 I>1 tReset',
                    'Value': value
                }
            else:
                self._tReset = {
                    'Setting': '383F',
                    'Description': 'T2 IN>1 tReset',
                    'Value': value
                }
        elif self.Terminal == 3:
            if self.Type == 'OC':
                self._tReset = {
                    'Setting': '354A',
                    'Description': 'T3 I>1 tReset',
                    'Value': value
                }
            else:
                self._tReset = {
                    'Setting': '386F',
                    'Description': 'T3 IN>1 tReset',
                    'Value': value
                }
        elif self.Terminal == 4:
            if self.Type == 'OC':
                self._tReset = {
                    'Setting': '356A',
                    'Description': 'T4 I>1 tReset',
                    'Value': value
                }
            else:
                self._tReset = {
                    'Setting': '389C',
                    'Description': 'T4 IN>1 tReset',
                    'Value': value
                }
        elif self.Terminal == 5:
            if self.Type == 'OC':
                self._tReset = {
                    'Setting': '358A',
                    'Description': 'T5 I>1 tReset',
                    'Value': value
                }
            else:
                self._tReset = {
                    'Setting': '38BC',
                    'Description': 'T5 IN>1 tReset',
                    'Value': value
                }
        elif self.Terminal == 6:
            if self.Type == 'OC':
                self._tReset = {
                    'Setting': '35AA',
                    'Description': 'T6 I>1 tReset',
                    'Value': value
                }
            else:
                self._tReset = {
                    'Setting': '38DC',
                    'Description': 'T6 IN>1 tReset',
                    'Value': value
                }
        else:
            if self.Type == 'OC':
                self._tReset = {
                    'Setting': '35CA',
                    'Description': 'T7 I>1 tReset',
                    'Value': value
                }
            else:
                self._tReset = {
                    'Setting': '38FC',
                    'Description': 'T7 IN>1 tReset',
                    'Value': value
                }

    @property
    def HighsetPickup(self):
        return self._HighsetPickup

    @HighsetPickup.setter
    def HighsetPickup(self, value):
        if value == 'Disabled':
            Status = 'Disabled'
            value = self.CTPrimary
        else:
            Status = 'DT'

        if not isinstance(value, (float, int)):
            raise ValueError('Please enter a number')

        value = value / self.CTPrimary

        if not value >= 0.08:
            raise ValueError('Entry must be in range 0.08 to 10')
        if not value <= 10:
            raise ValueError('Entry must be in range 0.08 to 10')

        value = value * self.CTSecondary

        if self.Terminal == 1:
            if self.Type == 'OC':
                self._HighsetPickup = {
                    'Setting': '350D',
                    'Description': 'T1 I>2 Current Set',
                    'Value': value
                }
                self._HighsetFunction = {
                    'Setting': '350B',
                    'Description': 'T1 I>2 Function',
                    'Value': Status
                }
            else:
                self._HighsetPickup = {
                    'Setting': '3813',
                    'Description': 'T1 IN>2 Current Set',
                    'Value': value
                }
                self._HighsetFunction = {
                    'Setting': '3811',
                    'Description': 'T1 IN>2 Function',
                    'Value': Status
                }
        elif self.Terminal == 2:
            if self.Type == 'OC':
                self._HighsetPickup = {
                    'Setting': '352D',
                    'Description': 'T2 I>2 Current Set',
                    'Value': value
                }
                self._HighsetFunction = {
                    'Setting': '352B',
                    'Description': 'T2 I>2 Function',
                    'Value': Status
                }
            else:
                self._HighsetPickup = {
                    'Setting': '3843',
                    'Description': 'T2 IN>2 Current Set',
                    'Value': value
                }
                self._HighsetFunction = {
                    'Setting': '3841',
                    'Description': 'T2 IN>2 Function',
                    'Value': Status
                }
        elif self.Terminal == 3:
            if self.Type == 'OC':
                self._HighsetPickup = {
                    'Setting': '354D',
                    'Description': 'T3 I>2 Current Set',
                    'Value': value
                }
                self._HighsetFunction = {
                    'Setting': '354B',
                    'Description': 'T3 I>2 Function',
                    'Value': Status
                }
            else:
                self._HighsetPickup = {
                    'Setting': '3873',
                    'Description': 'T3 IN>2 Current Set',
                    'Value': value
                }
                self._HighsetFunction = {
                    'Setting': '3871',
                    'Description': 'T3 IN>2 Function',
                    'Value': Status
                }
        elif self.Terminal == 4:
            if self.Type == 'OC':
                self._HighsetPickup = {
                    'Setting': '356D',
                    'Description': 'T4 I>2 Current Set',
                    'Value': value
                }
                self._HighsetFunction = {
                    'Setting': '356B',
                    'Description': 'T4 I>2 Function',
                    'Value': Status
                }
            else:
                self._HighsetPickup = {
                    'Setting': '38A2',
                    'Description': 'T4 IN>2 Current Set',
                    'Value': value
                }
                self._HighsetFunction = {
                    'Setting': '38A0',
                    'Description': 'T4 IN>2 Function',
                    'Value': Status
                }
        elif self.Terminal == 5:
            if self.Type == 'OC':
                self._HighsetPickup = {
                    'Setting': '358D',
                    'Description': 'T5 I>2 Current Set',
                    'Value': value
                }
                self._HighsetFunction = {
                    'Setting': '358B',
                    'Description': 'T5 I>2 Function',
                    'Value': Status
                }
            else:
                self._HighsetPickup = {
                    'Setting': '38C2',
                    'Description': 'T5 IN>2 Current Set',
                    'Value': value
                }
                self._HighsetFunction = {
                    'Setting': '38C0',
                    'Description': 'T5 IN>2 Function',
                    'Value': Status
                }
        elif self.Terminal == 6:
            if self.Type == 'OC':
                self._HighsetPickup = {
                    'Setting': '35AD',
                    'Description': 'T6 I>2 Current Set',
                    'Value': value
                }
                self._HighsetFunction = {
                    'Setting': '35AB',
                    'Description': 'T6 I>2 Function',
                    'Value': Status
                }
            else:
                self._HighsetPickup = {
                    'Setting': '38E2',
                    'Description': 'T6 IN>2 Current Set',
                    'Value': value
                }
                self._HighsetFunction = {
                    'Setting': '38E0',
                    'Description': 'T6 IN>2 Function',
                    'Value': Status
                }
        else:
            if self.Type == 'OC':
                self._HighsetPickup = {
                    'Setting': '35CD',
                    'Description': 'T7 I>2 Current Set',
                    'Value': value
                }
                self._HighsetFunction = {
                    'Setting': '35CB',
                    'Description': 'T7 I>2 Function',
                    'Value': Status
                }
            else:
                self._HighsetPickup = {
                    'Setting': '38FE',
                    'Description': 'T7 IN>2 Current Set',
                    'Value': value
                }
                self._HighsetFunction = {
                    'Setting': '38FD',
                    'Description': 'T2 IN>2 Function',
                    'Value': Status
                }

    @property
    def IDMTPickup(self):
        return self._IDMTPickup

    @IDMTPickup.setter
    def IDMTPickup(self, value):
        if value is None:
            value = self.CTPrimary

        if not isinstance(value, (float, int)):
            raise ValueError('Please enter a number')

        value = value / self.CTPrimary

        if not value >= 0.08:
            raise ValueError('Entry must be in range 0.08 to 4')
        if not value <= 4:
            raise ValueError('Entry must be in range 0.08 to 4')

        value = value * self.CTSecondary

        if self.Terminal == 1:
            if self.Type == 'OC':
                self._IDMTPickup = {
                    'Setting': '3504',
                    'Description': 'T1 I>1 Current Set',
                    'Value': value
                }
            else:
                self._IDMTPickup = {
                    'Setting': '3806',
                    'Description': 'T1 IN>1 Current Set',
                    'Value': value
                }
        elif self.Terminal == 2:
            if self.Type == 'OC':
                self._IDMTPickup = {
                    'Setting': '3524',
                    'Description': 'T2 I>1 Current Set',
                    'Value': value
                }
            else:
                self._IDMTPickup = {
                    'Setting': '3836',
                    'Description': 'T2 IN>1 Current Set',
                    'Value': value
                }
        elif self.Terminal == 3:
            if self.Type == 'OC':
                self._IDMTPickup = {
                    'Setting': '3544',
                    'Description': 'T3 I>1 Current Set',
                    'Value': value
                }
            else:
                self._IDMTPickup = {
                    'Setting': '3866',
                    'Description': 'T3 IN>1 Current Set',
                    'Value': value
                }
        elif self.Terminal == 4:
            if self.Type == 'OC':
                self._IDMTPickup = {
                    'Setting': '3564',
                    'Description': 'T4 I>1 Current Set',
                    'Value': value
                }
            else:
                self._IDMTPickup = {
                    'Setting': '3893',
                    'Description': 'T4 IN>1 Current Set',
                    'Value': value
                }
        elif self.Terminal == 5:
            if self.Type == 'OC':
                self._IDMTPickup = {
                    'Setting': '3584',
                    'Description': 'T5 I>1 Current Set',
                    'Value': value
                }
            else:
                self._IDMTPickup = {
                    'Setting': '38B3',
                    'Description': 'T5 IN>1 Current Set',
                    'Value': value
                }
        elif self.Terminal == 6:
            if self.Type == 'OC':
                self._IDMTPickup = {
                    'Setting': '35A4',
                    'Description': 'T6 I>1 Current Set',
                    'Value': value
                }
            else:
                self._IDMTPickup = {
                    'Setting': '38D3',
                    'Description': 'T6 IN>1 Current Set',
                    'Value': value
                }
        else:
            if self.Type == 'OC':
                self._IDMTPickup = {
                    'Setting': '35C4',
                    'Description': 'T7 I>1 Current Set',
                    'Value': value
                }
            else:
                self._IDMTPickup = {
                    'Setting': '38E2',
                    'Description': 'T7 IN>1 Current Set',
                    'Value': value
                }

    @property
    def HighsetDelay(self):
        return self._HighsetDelay

    @HighsetDelay.setter
    def HighsetDelay(self, value):
        if not isinstance(value, (float, int)):
            raise ValueError('Please enter a number')
        if not value >= 0:
            raise ValueError('Entry must be in range 0 to 100s')
        if not value <= 100:
            raise ValueError('Entry must be in range 0 to 100s')

        if self.Terminal == 1:
            if self.Type == 'OC':
                self._HighsetDelay = {
                    'Setting': '350E',
                    'Description': 'T1 I>2 Time Delay',
                    'Value': value
                }
            else:
                self._HighsetDelay = {
                    'Setting': '3815',
                    'Description': 'T1 IN>2 Time Delay',
                    'Value': value
                }
        elif self.Terminal == 2:
            if self.Type == 'OC':
                self._HighsetDelay = {
                    'Setting': '352E',
                    'Description': 'T2 I>2 Time Delay',
                    'Value': value
                }
            else:
                self._HighsetDelay = {
                    'Setting': '3845',
                    'Description': 'T2 IN>2 Time Delay',
                    'Value': value
                }
        elif self.Terminal == 3:
            if self.Type == 'OC':
                self._HighsetDelay = {
                    'Setting': '354E',
                    'Description': 'T3 I>2 Time Delay',
                    'Value': value
                }
            else:
                self._HighsetDelay = {
                    'Setting': '3875',
                    'Description': 'T3 IN>2 Time Delay',
                    'Value': value
                }
        elif self.Terminal == 4:
            if self.Type == 'OC':
                self._HighsetDelay = {
                    'Setting': '356E',
                    'Description': 'T4 I>2 Time Delay',
                    'Value': value
                }
            else:
                self._HighsetDelay = {
                    'Setting': '38A4',
                    'Description': 'T4 IN>2 Time Delay',
                    'Value': value
                }
        elif self.Terminal == 5:
            if self.Type == 'OC':
                self._HighsetDelay = {
                    'Setting': '358E',
                    'Description': 'T5 I>2 Time Delay',
                    'Value': value
                }
            else:
                self._HighsetDelay = {
                    'Setting': '38C4',
                    'Description': 'T5 IN>2 Time Delay',
                    'Value': value
                }
        elif self.Terminal == 6:
            if self.Type == 'OC':
                self._HighsetDelay = {
                    'Setting': '35AE',
                    'Description': 'T6 I>2 Time Delay',
                    'Value': value
                }
            else:
                self._HighsetDelay = {
                    'Setting': '38E4',
                    'Description': 'T6 IN>2 Time Delay',
                    'Value': value
                }
        else:
            if self.Type == 'OC':
                self._HighsetDelay = {
                    'Setting': '35CE',
                    'Description': 'T7 I>2 Time Delay',
                    'Value': value
                }
            else:
                self._HighsetDelay = {
                    'Setting': '38FF',
                    'Description': 'T7 IN>2 Time Delay',
                    'Value': value
                }


class PDF(object):
    def __init__(self, pdf, size=(900, 600)):
        self.pdf = pdf.replace(' ', '%20')
        self.size = size

    def _repr_html_(self):
        return '<iframe src={0} width={1[0]} height={1[1]}></iframe>'.format(
            self.pdf, self.size)

    def _repr_latex_(self):
        return r'\includegraphics[width=1.0\textwidth]{{{0}}}'.format(self.pdf)

