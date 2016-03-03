#!/usr/bin/env python3
from __future__ import print_function

import RPi.GPIO as GPIO
import json
from b3 import Client


led_pin = 17
button_pin = 27
state_open = False

server = "ws://192.168.0.42:8080"
token = "+-5OWDW8sS;bUPoDq-W5-d4i=/qTReG1"

client = Client(server, token)


def pressed(pin):
    "Button pressed"
    print("pressed")
    client.send({"state": {"open": not state_open}})


@client.on_message
def on_message(message):
    diff = json.loads(message)
    client.data.update(diff)
    print("on message", message)
    print("new data is:", client.data)

    global state_open
    state_open = client.data["state"]["open"]
    print("state_open is:", state_open)

    def green():
        GPIO.output(led_pin, GPIO.HIGH)

    def red():
        GPIO.output(led_pin, GPIO.LOW)

    if state_open:
        green()
    else:
        red()

# setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)
GPIO.setup(button_pin, GPIO.IN)
GPIO.add_event_detect(button_pin, GPIO.RISING,
                      callback=pressed, bouncetime=200)
#

client.start()
