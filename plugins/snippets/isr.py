#!/usr/bin/env python3

import RPi.GPIO as GPIO

def my_callback(channel):
	print("PUSH!")

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN)

GPIO.add_event_detect(27, GPIO.FALLING, callback=my_callback, bouncetime=10)

input()
