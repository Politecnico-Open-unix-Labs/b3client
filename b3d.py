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
    for name, plug in plugins.items():
        plug.setup(name)

    start_websocket()


def stop():
    for plug in plugins.values():
        plug.cleanup()


def dispatch(ws):
    for name, plug in plugins.items():
        plug_data = data.get(name, {})
        plug.handle(plug_data, ws)


def on_message(ws, message):
    diff = json.loads(message)
    data.update(diff)

    log.info(diff)

    dispatch(ws)


def on_error(ws, error):
    log.error("Error: %", error.message)
    log.info("Reconnecting...")
    start_websocket()


def on_close(ws):
    log.info("Connection closed")
    stop()


def on_open(ws):
    def ping():
        ws.send(json.dumps({"test": 123, "key": "antani"}))  # sample
        while 1:
            ws.send("{}")  # ping to avoid timeout
            time.sleep(15)

    Thread(target=ping).start()


def start_websocket():
    ws = websocket.WebSocketApp("ws://localhost:8080",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                on_open=on_open)
    ws.run_forever()


if __name__ == "__main__":
    start()
