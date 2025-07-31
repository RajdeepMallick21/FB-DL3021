#!/usr/bin/env python3
from DL3021 import DL3021
import pyvisa


if __name__=="__main__":
        
        '''Manually Sending Current Data'''
        
        modeSet = "CURRENT"
        power = 0
        current = 0

        # Slew Rate settings for corresponding Current Range:
        # 2.5A/us is max for 40A range
        # 0.25A/us is max for 4A range
        slewRate = 2.5
        rangeVal = 6

        rm = pyvisa.ResourceManager()
        res = rm.open_resource('USB0::6833::3601::DL3A26CM00318::0::INSTR')
        DL3021load = DL3021(res=res, 
                            mode_set=modeSet, 
                            power=power, 
                            current=current, 
                            slew_rate=slewRate,
                            range_val=rangeVal)

        filename = "conv.csv"
        DL3021load.fileRead(filename=filename)

        try:
                print("Attempting Send Sequence")
                DL3021load.loadSndSqnce(modeSet)
                

        except KeyboardInterrupt:
                print("Program Exited Manually")
