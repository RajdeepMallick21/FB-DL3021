import csv
import time

class csvConverter():
        def __init__(self, inFile, outFile, samplesToAvg):

                self.inFile = inFile
                self.outFile = outFile
                self.samplesToAvg = samplesToAvg

                self.origValsInterval = 0
                self.timeVals = []
                self.modeVals = []

                self.newTimeVals = []
                self.newModeVals = []

                
        def calcAvg(self):
                tempModeVal = 0
                
                for i in range(len(self.modeVals)):
                        # print(i)
                        # print("Adding Mode Values in Temp")
                        tempModeVal += self.modeVals[i]

                        if (i % self.samplesToAvg == 0):
                                self.newTimeVals.append(self.timeVals[i])
                                # print("Storing Time Value")

                        if (i % self.samplesToAvg == self.samplesToAvg - 1):
                                # print("Stopping and Taking Average")
                                tempModeVal /= self.samplesToAvg
                                self.newModeVals.append(tempModeVal)
                                tempModeVal = 0

                if tempModeVal != 0:
                        tempModeVal /= self.samplesToAvg
                        self.newModeVals.append(tempModeVal)
        
        def fileRead(self):
                print(f"Reading File: {self.inFile}")
                with open(file = self.inFile, newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
                        next(reader)
                        for row in reader:
                                self.timeVals.append(float(row[0]))
                                self.modeVals.append(round(abs(float(row[1])), 3))
                
                print("DONE Reading File")
                self.origValsInterval = self.timeVals[1] - self.timeVals[0]
        
        def fileWrite(self):
                print(f"Writing File:  {self.outFile}")
                with open(file=self.outFile, mode='w', newline='') as csvfile:
                        writer = csv.writer(csvfile, delimiter=',', quotechar='|',
                                                quoting=csv.QUOTE_MINIMAL)
                        for i in range(len(self.newTimeVals)):
                                writer.writerow([self.newTimeVals[i], self.newModeVals[i]])
                print("DONE Writing File")
                
        

if __name__ == "__main__":
          testConv = csvConverter(inFile="Main current - Ace.csv",
                                   outFile="conv.csv",
                                   samplesToAvg = 100)
          testConv.fileRead()
          testConv.calcAvg()
          testConv.fileWrite()
