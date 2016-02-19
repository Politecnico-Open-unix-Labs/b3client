#!/usr/bin/env python3
from __future__ import print_function
import json
import time
import logging
from threading import Thread
from websocket import WebSocketApp
import RPi.GPIO as GPIO

import config


# import config from: $HOME/.b3d and /etc/b3d
# import os.path
# home_path = os.path.join(os.path.expanduser("~"), ".b3d")
# etc_path = os.path.join("/etc", "b3d")

# import sys
# sys.path.append(home_path)
# sys.path.append(etc_path)

# import config


# Inizialize logging
log_level = getattr(logging, config.log_level.upper(), None)

logging.basicConfig(level=log_level)
log = logging.getLogger(__name__)

log_fd = logging.FileHandler(config.log_file, "w")
log_fd.setLevel(log_level)
log.addHandler(log_fd)
#


data = {}
ws = None

led_pin = 17
button_pin = 27
state_open = False


def send(msg):
    "Send msg (a dict) to the server"

    if not ws:
        return

    ws.send(json.dumps(dict(msg, **{"key": config.token})))


def start_websocket():
    log.info("Starting websocket")
    global ws
    ws = WebSocketApp(config.server, [],
                      on_open, on_message, on_error, on_close)

    ws.run_forever()


def on_message(ws, message):
    diff = json.loads(message)
    data.update(diff)
    print("on message", message)
    print("new data is:", data)

    global state_open
    state_open = data["state"]["open"]
    print("state_open is:", state_open)

    def green():
        GPIO.output(led_pin, GPIO.HIGH)

    def red():
        GPIO.output(led_pin, GPIO.LOW)

    if state_open:
        green()
    else:
        red()


def on_error(ws, error):
    "Restart websocket"
    log.error("Error: %s", error)
    time.sleep(1)
    log.info("Reconnecting...")
    start_websocket()


def on_close(ws):
    "On connection close, cleanup things"
    log.info("Connection closed")


def on_open(ws):
    "Send empty jsons to keep alive the connection, on an separate thread"
    def channel():
        while True:
            ws.send("{}")  # ping to avoid timeout
            time.sleep(15)

    Thread(target=channel).start()


def pressed(pin):
    "Button pressed"
    print("pressed")
    send({"state": {"open": not state_open}})


if __name__ == "__main__":
    # setup
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(led_pin, GPIO.OUT)
    GPIO.setup(button_pin, GPIO.IN)
    GPIO.add_event_detect(button_pin, GPIO.RISING,
                          callback=pressed, bouncetime=200)
    #

    start_websocket()
