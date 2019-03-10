#!/usr/bin/python3
import serial
import logging
import threading
from time import sleep

#~10 minute cycle time
PUMP_ON_TIME = 60*2+30
PUMP_OFF_TIME = 60*7+30


class Controls:
	def __init__(self, logger):
		self.outlets = serial.Serial("/dev/serial0", baudrate=115200, timeout=3.0)
		self.logger = logger
		self.serialMutex = threading.Lock()
		self.logger.debug('controls started')

	def lightsOn(self):
		with self.serialMutex:
			#self.outlets.write(b'2+')
			pass
		self.logger.info('Lights on')
	def ligstOff(self):
		with self.serialMutex:
			#self.outlets.write(b'2-')
			pass
		self.logger.info('Lights off')

	def pumpOn(self):
		with self.serialMutex:
			#self.outlets.write(b'1+')
			pass
		self.logger.info('Pump on')

	def pumpOff(self):
		with self.serialMutex:
			#self.outlets.write(b'1-')
			pass
		self.logger.info('Pump off')

def pump(controls):
	while True:
		controls.pumpOn()
		sleep(PUMP_ON_TIME)
		controls.pumpOff()
		sleep(PUMP_OFF_TIME)

def main():
	#setup the logger
	logging.basicConfig(filename="test.log", 
	                    format='%(asctime)s: %(levelname)s: %(message)s', 
	                    filemode='a') 
	logger=logging.getLogger() 
	logger.setLevel(logging.DEBUG) 
	logger.debug('Application started')
	controls = Controls(logger)

	#create thread to control the pump
	pumpThread = threading.Thread(target=pump, args=(controls,))
	pumpThread.daemon = True
	pumpThread.start()

	#create thread to control the lights


	#let the threads work
	while True:
		sleep(1000)


if __name__ == '__main__':
	main()
