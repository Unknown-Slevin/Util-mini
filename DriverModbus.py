import serial
import minimalmodbus

from time import sleep
class DriverModbus:



    def __init__(self, address=1, port='COM8', baudrate=115200, bytesize=8, parity=serial.PARITY_NONE, stopbits=1, timeout=0.1):
        self.client1 = minimalmodbus.Instrument(port, address, debug=False)  # port name, slave address (in decimal)
        self.client1.serial.baudrate = baudrate  # baudrate
        self.client1.serial.bytesize = bytesize
        self.client1.serial.parity   = parity
        self.client1.serial.stopbits = stopbits
        self.client1.serial.timeout  = timeout      # seconds
        self.client1.address         = address        # this is the slave address number
        self.client1.mode = minimalmodbus.MODE_RTU # rtu or ascii mode
        self.client1.clear_buffers_before_each_transaction = True


    def readMemoryModbus(self, num_reg):
        kp = self.client1.read_register(num_reg)  # read single register 2bytes (16bit)
        print("Kp: ", kp)


    def writeMemoryModbus(self, num_reg, value):

        if (num_reg != None):
            print(f"nume reg: {num_reg}, value: {value}")
            self.client1.write_register(num_reg, value, number_of_decimals=0, functioncode=6)

    def writeLong(self, reg, value):
        self.client1.write_long(reg, value)

    def sendCortage(self, data):
        length = len(data)

        for i in range(1, length):
            if (i < 4):
                self.writeMemoryModbus(data[length - 1][i - 1], data[i - 1])
                sleep(0.005)

    def sendArrayDataToPLC(self, data, length0):
        length = length0

        for i in range(1, length + 1):
            self.sendCortage(data[i - 1])
            print(f"i: {i}")

        return 0

    def setAdress(self, id):
        self.client1.address = id

    def setBaudRate(self, baud_rate):
        self.client1.serial.baudrate = baud_rate

    def setParity(self, parity):
        self.client1.serial.parity = parity