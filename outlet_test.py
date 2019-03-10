#!/usr/bin/python3

import serial
from time import sleep

port = serial.Serial("/dev/serial0", baudrate=115200, timeout=3.0)

while True:
    port.write(b'1+')
    for i in range(150):
    	print(i)
    	sleep(1)
    port.write(b'-')
    sleep(60*7+30)