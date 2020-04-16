import RPi.GPIO as GPIO
from time import sleep
PWM_PIM = 19
GPIO.setmode(GPIO.BCM)
GPIO.setup(PWM_PIM, GPIO.OUT)
p = GPIO.PWM(PWM_PIM, 25000)

p.start(50)

while True:
    for x in range(100):    
        p.ChangeDutyCycle(x)
        sleep(0.05)
    for x in range(100):
        p.ChangeDutyCycle(100 - x)
        sleep(0.05)