#!/usr/bin/python3
import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime
channel = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
last = 0
while True:
	if last != GPIO.input(channel):
		print(GPIO.input(channel))
		last = GPIO.input(channel)

	sleep(0.5)

