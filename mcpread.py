import spidev
from time import sleep

class Mcp:
    def __init__(self):
        self.spi = spidev.SpiDev()
        self.spi.open(0,1)
        self.spi.max_speed_hz = 1350000

    def read(self, channel):
        adc = self.spi.xfer2([1,(8+channel)<<4,0])
        data = ((adc[1]&3) << 8) + adc[2]
        return data

if __name__ == "__main__":
    mcp = Mcp()
    while True:
        print([ mcp.read(c) for c in range(8) ])
        sleep(0.5)     