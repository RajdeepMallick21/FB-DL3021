import pyvisa
from LabInstruments.DL3000 import DL3000
import time
import csv

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
                                self.timeVals.append(float(row[0]))
                                self.modeVals.append(round(abs(float(row[1])), 3))
                
                self.sendInterval = self.timeVals[1] - self.timeVals[0]
                print(f"Send Interval: {self.sendInterval}")
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
