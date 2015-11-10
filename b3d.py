#!/usr/bin/env python3
import json
import time
import logging
from threading import Thread
from websocket import WebSocketApp


# import config and plugins from: $HOME/.b3d and /etc/b3d
import os.path
home_path = os.path.join(os.path.expanduser("~"), ".b3d")
etc_path = os.path.join("/etc", "b3d")

import sys
sys.path.append(home_path)
sys.path.append(etc_path)

import config


def get_plugin(name):
    "Dynamically: from  plugins import plugin_name"
    module = __import__("plugins", fromlist=[name])
    return module.__dict__[name]

plugins = [get_plugin(name).Plugin()
           for name in config.plugins]

log_level = getattr(logging, config.log_level.upper(), None)

logging.basicConfig(level=log_level)
log = logging.getLogger(__name__)

log.propagate = False  # hide logs from stdout
log_fd = logging.FileHandler(config.log_file, "w")
log_fd.setLevel(log_level)
log.addHandler(log_fd)


data = {}


def start():
    "Setup plugins and start websocket"

    for plug in plugins:
        plug.setup()

    start_websocket()


def start_websocket():
    log.info("Starting websocket")
    ws = WebSocketApp(config.server, [],
                      on_open, on_message, on_error, on_close)

    def send(msg):
        "Send msg (a dict) to the server"
        ws.send(json.dumps(dict(msg, **{"key": config.token})))

    for plug in plugins:
        plug.send = send

    ws.run_forever()


def on_message(ws, message):
    """Update the local data and dispatch changes to plugins, passing ws because
    some plugins should be able to send changes to server"""
    diff = json.loads(message)
    data.update(diff)

    log.info("recived %s", diff)

    for plug in plugins:
        name = plug.name
        plug_diff = diff.get(name, None)
        if plug_diff:
            log.info("dispatching %s to %s", str(data[name]), name)
            plug.handle(data[name])


def on_error(ws, error):
    "Restart websocket"
    log.error("Error: %s", error)
    time.sleep(1)
    log.info("Reconnecting...")
    start_websocket()


def on_close(ws):
    "On connection close, cleanup plugins"
    log.info("Connection closed")
    for plug in plugins:
        plug.clean()


def on_open(ws):
    "Send empty jsons to keep alive the connection, on an separate thread"
    def channel():
        while True:
            ws.send("{}")  # ping to avoid timeout
            time.sleep(15)

    Thread(target=channel).start()


if __name__ == "__main__":
    start()
