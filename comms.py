#!/usr/bin/env python3
from DL3021 import DL3021
import pyvisa
import time


if __name__=="__main__":
        
        modeSend = input("Enter modeSend\nChoose from [Continuous, Burst, File]\n")

        # Setting Load mode and initial output values
        modeSet = "CURRENT"
        power = 0
        current = 0

        # Slew Rate settings for corresponding Current Range:
        # 2.5A/us is max for 40A range
        # 0.25A/us is max for 4A range
        slewRate = 2.5
        rangeVal = 6

        # Finding resource(instrument) from pyvisa resource manager
        # Using found resource to create object of DL3021 class
        rm = pyvisa.ResourceManager()
        res = rm.open_resource('USB0::6833::3601::DL3A26CM00318::0::INSTR')
        DL3021load = DL3021(res=res, 
                            mode_set=modeSet, 
                            power=power, 
                            current=current, 
                            slew_rate=slewRate,
                            range_val=rangeVal)

        # File with averaged output values
        filename = "conv.csv"
        DL3021load.fileRead(filename=filename)
        

        match modeSend:
                case "1":
                        t_period = float(input("t_period in seconds\n"))
                        current_step = float(input("Current step in Amps\n"))
                        current = float(input("Initial current value in Amps\n"))
                        current_limit = float(input("Upper current limit in Amps\n"))

                        DL3021load.DL3KOBJ.set_cc_current(current)
                        v_init = DL3021load.DL3KOBJ.voltage()
                        DL3021load.DL3KOBJ.enable()
                        
                        while ((DL3021load.DL3KOBJ.voltage()/v_init) > 0.80
                               and (current < current_limit)):
                                try:
                                        time.sleep(t_period)
                                        current += current_step
                                        DL3021load.DL3KOBJ.set_cc_current(
                                                current
                                        )
                                        print(f'Set C: {current}')
                                        print(f'Load C: {DL3021load.DL3KOBJ.current()}')
                                        
                                        if (DL3021load.DL3KOBJ.voltage() / v_init) < 0.80:

                                                print("Voltage Out Of Spec")
                                                print(DL3021load.DL3KOBJ.current())
                                       
                                except KeyboardInterrupt:
                                        print("Ending Program Manually")
                                        DL3021load.DL3KOBJ.disable()
                                        break
                                        

                        DL3021load.DL3KOBJ.disable()
                        
                
                case "2":
                        idle_current = float(input("Idle current in Amps\n"))
                        t_period = float(input("t_period in seconds\n"))
                        temp_t_period = t_period
                        t_period_decrement = float(input("Decrement value for t_period in seconds\n"))
                        burst_current_list = map(float, input("Burst current in Amps\n").split())
                        t_blip = float(input("t_blip in seconds\n"))
                        
                        DL3021load.DL3KOBJ.enable()
                        try:    
                                for burst_current in burst_current_list:
                                        while(temp_t_period > 0):
                                                DL3021load.DL3KOBJ.set_cc_current(idle_current)
                                                time.sleep(temp_t_period)
                                                DL3021load.DL3KOBJ.set_cc_current(burst_current)
                                                time.sleep(t_blip)
                                                temp_t_period -= t_period_decrement
                                        
                                        DL3021load.DL3KOBJ.set_cc_current(burst_current)
                                        temp_t_period = t_period
                                        time.sleep(temp_t_period)
                                        idle_current = burst_current                                      

                        except KeyboardInterrupt:
                                print("Ending Program Manually")
                                DL3021load.DL3KOBJ.disable()

                        DL3021load.DL3KOBJ.disable()
                                        

                case "3":
                        try:
                                print("Attempting Send Sequence")
                                DL3021load.loadSndSqnce(modeSet)
                        
                        except KeyboardInterrupt:
                                print("Program Exited Manually")
