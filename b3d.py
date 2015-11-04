#!/usr/bin/env python3
import json
import time
from threading import Thread
from websocket import WebSocketApp
import logging

from plugins import plugins
import config


logging.basicConfig(level=getattr(logging,
                                  config.loglevel.upper(),
                                  None))
log = logging.getLogger(__name__)


data = {}


def start():
    "Setup plugins and start websocket"

    log.info("Starting websocket")
    ws = WebSocketApp(config.server, [],
                      on_open, on_message, on_error, on_close)

    for name, plug in plugins.items():
        plug.setup(name, ws)

    ws.run_forever()


def on_message(ws, message):
    """Update the local data and dispatch changes to plugins, passing ws because
    some plugins should be able to send changes to server"""
    diff = json.loads(message)
    data.update(diff)

    log.info(diff)

    for name, plug in plugins.items():
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
    for plug in plugins.values():
        plug.cleanup()


def on_open(ws):
    "Send empty jsons to keep alive the connection, on an separate thread"
    def channel():
        # ws.send(json.dumps({"test": 123, "key": "antani"}))  # sample
        while True:
            ws.send("{}")  # ping to avoid timeout
            time.sleep(15)

    Thread(target=channel).start()


if __name__ == "__main__":
    start()
