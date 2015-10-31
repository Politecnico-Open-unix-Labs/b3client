#!/usr/bin/env python3
import websocket
import json
import time
from threading import Thread
import logging
from plugins import plugins

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


data = {}


def start():
    "Setup plugins and start websocket"
    for name, plug in plugins.items():
        plug.setup(name)

    start_websocket()


def on_message(ws, message):
    """Update the local data and dispatch changes to plugins, passing ws because
    some plugins should be able to send changes to server"""
    diff = json.loads(message)
    data.update(diff)

    log.info(diff)

    for name, plug in plugins.items():
        plug_diff = diff.get(name, None)
        if plug_diff:
            plug.handle(data[name], ws)


def on_error(ws, error):
    "Restart websocket"
    log.error("Error: %", error.message)
    log.info("Reconnecting...")
    start_websocket()


def on_close(ws):
    "On connection close, cleanup plugins"
    log.info("Connection closed")
    for plug in plugins.values():
        plug.cleanup()


def on_open(ws):
    "Send empty jsons to keep alive the connection, on an other thread"
    def ping():
        # ws.send(json.dumps({"test": 123, "key": "antani"}))  # sample
        while 1:
            ws.send("{}")  # ping to avoid timeout
            time.sleep(15)

    Thread(target=ping).start()


def start_websocket():
    "Start the websocket client on the main thread"
    ws = websocket.WebSocketApp("ws://localhost:8080",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                on_open=on_open)
    ws.run_forever()


if __name__ == "__main__":
    start()
