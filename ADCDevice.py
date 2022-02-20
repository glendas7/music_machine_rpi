import smbus

class ADCDevice(object):
    def __init__(self):
        self.cmd = 0
        self.address = 0
        self.bus=smbus.SMBus(1)

    def close(self):
        self.bus.close()
    

class ADS7830(ADCDevice):
    def __init__(self):
        super(ADS7830, self).__init__()
        self.cmd = 0x84
        self.address = 0x4b
        
    def analogRead(self, chn): 
        value = self.bus.read_byte_data(self.address, self.cmd|(((chn<<2 | chn>>1)&0x07)<<4))
        return value
