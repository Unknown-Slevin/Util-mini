

LENGTH_DATA_OUTPUT = 5
POSITION_BIN_DIGITAL_OUTPUT = 3
class DataPLC:

    def __init__(self):
        self.data = []
        self.length = 0
        self.bin_digital = 0

    def addData(self, item):
        self.data.append(item)
        self.length = self.length + 1

    def print(self):
        print(self.data)
        print(self.length)
        print((self.bin_digital))

    def setBinDigital(self):
        for i in range(1, self.length):
            if (len(self.data[i]) == LENGTH_DATA_OUTPUT):
                self.bin_digital = self.bin_digital | self.data[i][POSITION_BIN_DIGITAL_OUTPUT]


    def getBinDigital(self):
        return self.bin_digital

    def getData(self):
        return self.data

    def getLength(self):
        return self.length