#!/usr/bin/env python3
from LabInstruments.DL3000 import DL3000
import pyvisa
import csv
import time
import matplotlib.pyplot as plt

class DL3021:              

        def __init__(self, res, mode_set, power=0, current=0, slew_rate=0, range_val=4):
                self.DL3KOBJ = DL3000(res)
                self.modeVals = []
                self.timeVals = []
                self.sendInterval = 0

                match mode_set:
                        case "POWER":
                                self.DL3KOBJ.set_mode("POWER")
                                self.DL3KOBJ.set_cp_power(power)
                                print("Power Mode Set")
                        
                        case "CURRENT":
                                self.DL3KOBJ.set_mode("CC")
                                self.DL3KOBJ.set_cc_current(current)
                                self.DL3KOBJ.set_cc_range(range_val)
                                self.DL3KOBJ.set_cc_slew_rate(slew_rate)
                                print("Current Mode Set")
                                
        def fileRead(self, filename):
                print("Reading File")
                with open(file=filename, newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
                        next(reader)
                        for row in reader:
                        #         print(f'At Time: {row[0]}, Power is: {row[1]}')
                                self.timeVals.append(float(row[0]))
                                self.modeVals.append(round(abs(float(row[1])), 3))
                
                self.sendInterval = self.timeVals[1] - self.timeVals[0]
                print(f"Send Interval: {self.sendInterval}")
                # self.sendInterval = self.timeVals[1] - self.timeVals[0]
                # print(f"Calculated send interval: {self.sendInterval}")
                # print(f"Difference between max and min current values{abs(max(self.modeVals)) - abs(min(self.modeVals))}")
                # plt.plot(self.timeVals[0:512], self.modeVals[0:512])
                # plt.xlabel("Time")
                # plt.ylabel("Current Value")
                # plt.show()
                print("Done Reading")

        def loadSndSqnce(self, mode):
                self.DL3KOBJ.enable()
                        
                if mode == "CURRENT":
                        for val in self.modeVals:
                                self.DL3KOBJ.set_cc_current(current=val)
                                time.sleep(self.sendInterval)
                elif mode == "POWER":
                        for val in self.modeVals:
                                self.DL3KOBJ.set_cp_power(val)
                                time.sleep(self.sendInterval)
                
                self.DL3KOBJ.disable()
                

if __name__=="__main__":
        
        '''Manually Sending Current Data'''

        modeSet = "CURRENT"
        power = 0
        current = 0
        slewRate = 2.5
        rangeVal = 6
        # 2.5A/us is max for 40A range
        # 0.25A/us is max for 4A range

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
                # while True:
                #         print("Attempting Send Sequence")
                #         DL3021load.loadSndSqnce(modeSet)
                

        except KeyboardInterrupt:
                print("Program Exited Manually")

        
        
        '''Setting up List operation with sample data'''
        
        # modeSet = "CURRENT"
        # power = 0
        # current = 0
        # slewRate = 0.25

        # rm = pyvisa.ResourceManager()
        # res = rm.open_resource('USB0::6833::3601::DL3A26CM00318::0::INSTR')
        # DL3021load = DL3021(res=res, 
        #                     mode_set=modeSet, 
        #                     power=power, 
        #                     current=current, 
        #                     slew_rate=slewRate)

        # # filename = "Main current - Ace.csv"
        # # DL3021load.fileRead(filename=filename)
        
        # sampleList = [0.3, 0.2, 0.1]
        # sampleListLen = len(sampleList)

        # print("Setting up List operation")
        # DL3021load.DL3KOBJ.set_list_mode("CC")
        # time.sleep(0.5)
        # DL3021load.DL3KOBJ.set_list_range(6)
        # time.sleep(0.5)
        # DL3021load.DL3KOBJ.set_list_count_infinity()
        # time.sleep(0.5)
        # DL3021load.DL3KOBJ.set_list_step(steps=sampleListLen)
        # time.sleep(0.5)
        # DL3021load.DL3KOBJ.set_list_end(endState="OFF")
        # time.sleep(0.5)

        # DL3021load.DL3KOBJ.set_list_level(steps=sampleListLen, 
        #                                 levelList=sampleList)
        # time.sleep(0.5)
        # DL3021load.DL3KOBJ.set_list_width(steps=sampleListLen, 
        #                                 listWidth=2)
        # time.sleep(0.5)
        # DL3021load.DL3KOBJ.set_list_slew(steps=sampleListLen,
        #                                 listSlew=2.5)
        # time.sleep(0.5)
        # DL3021load.DL3KOBJ.enable()
        # time.sleep(1)
        
        # DL3021load.DL3KOBJ.trig_immediate()

        # # res.close()
        # # del res
        # # rm.close()
        # # del rm


        
        '''Manually Sending Current Data'''

        # modeSet = "CURRENT"
        # power = 0
        # current = 0
        # slewRate = 0.25
        # # 2.5A/us is max for 40A range
        # # 0.25A/us is max for 4A range

        # rm = pyvisa.ResourceManager()
        # res = rm.open_resource('USB0::6833::3601::DL3A26CM00318::0::INSTR')
        # DL3021load = DL3021(res=res, 
        #                     mode_set=modeSet, 
        #                     power=power, 
        #                     current=current, 
        #                     slew_rate=slewRate)

        # filename = "Main current - Ace.csv"
        # DL3021load.fileRead(filename=filename)

        # try:
        #         while True:
        #                 print("Attempting Send Sequence")
        #                 DL3021load.loadSndSqnce(modeSet, 20/1000000)

        # except KeyboardInterrupt:
        #         print("Program Exited Manually")


        '''Example from Programming Manual'''


        # rm = pyvisa.ResourceManager()
        # print(rm.list_resources())
        # res = rm.open_resource(rm.list_resources()[0])

        # print(res.query('*IDN?'))
        
        # res.write(":SOUR:LIST:MODE CC")
        # print("List Mode:")
        # print(res.query(":SOUR:LIST:MODE?"))
        
        # res.write("SOUR:LIST:RANG 6")
        # print("List Range:")
        # print(res.query(":SOUR:LIST:RANG?"))

        # res.write(":SOUR:LIST:COUN 2")
        # print("List Count:")
        # print(res.query(":SOUR:LIST:COUN?"))

        # res.write(":SOUR:LIST:STEP 2")
        # print("List Steps:")
        # print(res.query("SOUR:LIST:STEP?"))

        # res.write(":SOUR:LIST:END LAST")
        # print("List End State:")
        # print(res.query(":SOUR:LIST:END?"))

        # res.write(":SOUR:LIST:LEV 0,1")
        # print("List Level for Step 0")
        # print(res.query(":SOUR:LIST:LEV? 0"))

        # res.write(":SOUR:LIST:WID 0,3")
        # print(res.query(":SOUR:LIST:WID? 0"))

        # res.write(":SOUR:LIST:SLEW 0,0.1")
        # print(res.query(":SOUR:LIST:SLEW? 0"))
        
        # res.write(":SOUR:LIST:LEV 1,1.2")
        # print(res.query(":SOUR:LIST:LEV? 1"))
        
        # res.write(":SOUR:LIST:WID 1,5")
        # print(res.query(":SOUR:LIST:WID? 1"))
        
        # res.write(":SOUR:LIST:SLEW 1,0.3")
        # print(res.query(":SOUR:LIST:SLEW? 1"))
        
        # res.write(":SOUR:LIST:LEV 2,1.8")
        # print(res.query(":SOUR:LIST:LEV? 2"))
        
        # res.write(":SOUR:LIST:WID 2,3.5")
        # print(res.query(":SOUR:LIST:WID? 2"))
        
        # res.write(":SOUR:LIST:SLEW 2,0.2")
        # print(res.query(":SOUR:LIST:SLEW? 2"))
        
        # res.write(":TRIG:SOUR BUS")
        # print(res.query(":TRIG:SOUR?"))
        
        # res.write(":SOUR:INP:STAT 1")
        # print(res.query(":SOUR:INP:STAT?"))

        # time.sleep(1)
        # res.write(":TRIG:IMM")

        # ''' 
        # (1) *IDN? /*Queries the ID string of the load to test whether the remote
        # communication works normally.*/
        # (2) :SOUR:LIST:MODE CC /*Sets the operation mode of the load to be CC mode.*/
        # (3) :SOUR:LIST:RANG 6 /*Sets the load's current range in CC mode to be 6 A.*/
        # (4) :SOUR:LIST:COUN 2 /*Sets the number of times the list is cycled to be 2.*/
        # (5) :SOUR:LIST:STEP 2 /*Sets the total steps to be 3.*/
        # (6) :SOUR:LIST:END LAST /*Sets the end state of the load to be Last.*/
        # (7) :SOUR:LIST:LEV 0,1 /*Sets the input current setting at Step 1 to be 1 A.*/
        # (8) :SOUR:LIST:WID 0,3 /*Sets the dwell time at Step 1 to be 3 s.*/
        # (9) :SOUR:LIST:SLEW 0,0.1 /*Sets the slew rate at Step 1 to be 0.1 A/μs.*/
        # (10) :SOUR:LIST:LEV 1,1.2 /*Sets the input current setting at Step 2 to be 1.2 A.*/
        # (11) :SOUR:LIST:WID 1,5 /*Sets the dwell time at Step 2 to be 5 s.*/
        # (12) :SOUR:LIST:SLEW 1,0.3 /*Sets the slew rate at Step 2 to be 0.3 A/μs.*/
        # (13) :SOUR:LIST:LEV 2,1.8 /*Sets the input current setting at Step 3 to be 1.8 A.*/
        # (14) :SOUR:LIST:WID 2,3.5 /*Sets the dwell time at Step 3 to be 3.5 s.*/
        # (15) :SOUR:LIST:SLEW 2,0.2 /*Sets the slew rate at Step 3 to be 0.2 A/μs.*/
        # (16) :TRIG:SOUR MANU /*Sets the trigger source of the load to be manual. Pressing the TRAN
        # key can enable the trigger.*/
        # (17) :SOUR:INP:STAT 1 /*Sets the input of the load to be on.*/

        # '''



