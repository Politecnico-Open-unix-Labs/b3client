#!/usr/bin/env python3
from __future__ import print_function

import RPi.GPIO as GPIO
from b3 import Client


led_pin = 17
button_pin = 27
state_open = False

server = "ws://192.168.0.42:8080"
token = "+-5OWDW8sS;bUPoDq-W5-d4i=/qTReG1"

client = Client(server, token)


def green():
    GPIO.output(led_pin, GPIO.HIGH)


def red():
    GPIO.output(led_pin, GPIO.LOW)


def pressed(pin):
    "Button pressed"
    print("pressed")
    client.send("/state/open", not state_open)


@client.on_message("/state/open")
def on_message(value):
    print("state_open is:", value)

    if value:
        green()
    else:
        red()

    global state_open
    state_open = value


# setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)
GPIO.setup(button_pin, GPIO.IN)
GPIO.add_event_detect(button_pin, GPIO.RISING,
                      callback=pressed, bouncetime=200)
#

client.start()
