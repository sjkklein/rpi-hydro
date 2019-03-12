#!/usr/bin/python3

import RPi.GPIO as GPIO
from time import sleep
channel = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
while True:
	print(GPIO.input(channel))
sleep(0.5)

