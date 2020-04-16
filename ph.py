import mcpread
from time import sleep

class Ph:
    def __init__(self, channel):
        self.mcp = mcpread.Mcp()
        self.channel = channel
    
    def getPh(self):
        adcVal = self.mcp.read(self.channel)
        return adcVal

if __name__ == '__main__':
    ph = Ph(1)
    while True:
        print(ph.getPh())
        sleep(0.5)
