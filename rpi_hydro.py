#!/usr/bin/python3
import serial
import logging
import threading
from datetime import datetime	
from time import sleep
import RPi.GPIO as GPIO
from repeat_timer import RepeatedTimer
import requests


#~10 minute cycle time
PUMP_ON_TIME = 60*2+30
PUMP_OFF_TIME = 60*7+30
#~17 hour light cycle
LIGHTS_ON_HOUR = 4
LIGHTS_OFF_HOUR = 21 

FLOAT_SWITCH_PIN = 26

def send_notification(notification):
	payload = {
	  "app_key": "fq7BiSDaO5in2w6dGijW",
	  "app_secret": "x81t4jCpcYAQiKJAw5u8wSVrSDX1cJ6tTDG0qw988v5KOwu6KjZ6dRA0nhA4ii2I",
	  "target_type": "app",
	  "content": notification
	}
	r = requests.post("https://api.pushed.co/1/push", data=payload)
	print(notification)
	return r.text


class Controls:
	def __init__(self, logger):
		self.outlets = serial.Serial("/dev/serial0", baudrate=115200, timeout=3.0)
		self.logger = logger
		self.serialMutex = threading.Lock()
		self.logger.debug('controls started')
		#initialize with the lights on so we can track the state a bit easier
		self.lightsOnFlag = False
		self.lightsOn()

	def lightsOn(self):
		if  not self.lightsOnFlag:
			with self.serialMutex:
				self.outlets.write(b'2+')
				pass
			self.logger.info('Lights on')
			self.lightsOnFlag = True

	def lightsOff(self):
		if self.lightsOnFlag:
			with self.serialMutex:
				self.outlets.write(b'2-')
				pass
			self.logger.info('Lights off')
			self.lightsOnFlag = False

	def pumpOn(self):
		with self.serialMutex:
			self.outlets.write(b'1+')
			pass
		self.logger.info('Pump on')

	def pumpOff(self):
		with self.serialMutex:
			self.outlets.write(b'1-')
			pass
		self.logger.info('Pump off')

def pump(controls):
	while True:
		controls.pumpOn()
		sleep(PUMP_ON_TIME)
		controls.pumpOff()
		sleep(PUMP_OFF_TIME)

def lights(controls):
	while True:
		hour = datetime.now().hour
		if hour >= LIGHTS_ON_HOUR and hour < LIGHTS_OFF_HOUR:
			controls.lightsOn()
		else:
			controls.lightsOff()
		sleep(30)

def init_alarm_pin():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(FLOAT_SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

alarm_str=""
def push():
	global alarm_str
	send_notification(alarm_str)

def alarm(logger):
	global alarm_str
	#init last level to be differnet than the level
	if GPIO.input(FLOAT_SWITCH_PIN) == 1:
		last_level = 0
	else:
		last_level = 1
	#create timer to send notification
	cycle = PUMP_OFF_TIME + PUMP_ON_TIME
	alarmTimer = RepeatedTimer(cycle * 3, push)

	while True:
		level = GPIO.input(FLOAT_SWITCH_PIN)
		if level != last_level:
			alarmTimer.stop()
			alarmTimer.start()
			last_level = level
			if level == 1:
				alarm_str = "likely pump overflow"
				logger.info("water high")
			else:
				alarm_str = "pump probably not running"
				logger.info("water low")
		sleep(0.1)


def main():
	#setup the logger
	logging.basicConfig(filename="events.log", 
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
	lightsThread = threading.Thread(target=lights, args=(controls,))
	lightsThread.daemon = True
	lightsThread.start()

	#create thread to detect alerts and send notifications
	init_alarm_pin()
	alarmThread = threading.Thread(target=alarm, args=(logger,))
	alarmThread.daemon = True
	alarmThread.start()
	#let the threads work
	while True:
		sleep(1000000)


if __name__ == '__main__':
	main()
