import csv

class csvConverter():
          def __init__(self, inFile, outFile):
                    self.inFile = inFile
                    self.outFile = outFile
                    self.valsInterval = 0
                    self.timeVals = []
                    self.modeVals = []

                    
          def fileRead(self):
                    print(f"Reading File: {self.inFile}")
                    with open(file = self.inFile, newline='') as csvfile:
                              reader = csv.reader(csvfile, delimiter=',', quotechar='|')
                              next(reader)
                              for row in reader:
                                        self.timeVals.append(float(row[0]))
                                        self.modeVals.append(round(abs(float(row[1])), 3))
                    
                    print("DONE Reading File")
                    self.valsInterval = self.timeVals[1] - self.timeVals[0]
          
          def fileWrite(self):
                    print(f"Writing File:  {self.outFile}")
                    with open(file=self.outFile, mode='w', newline='') as csvfile:
                              writer = csv.writer(csvfile, delimiter=',', quotechar='|',
                                                  quoting=csv.QUOTE_MINIMAL)
                              for i in range(len(self.timeVals)):
                                        writer.writerow([self.timeVals[i], self.modeVals[i]])
                    print("DONE Writing File")
                  
          

if __name__ == "__main__":
          testConv = csvConverter(inFile="Main current - Ace.csv",
                                   outFile="conv.csv")
          testConv.fileRead()
          testConv.fileWrite()
