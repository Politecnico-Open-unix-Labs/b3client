#!/usr/bin/env python3
import websocket
import json
import time
from threading import Thread

from plugins import plugins


data = {}


def start():
    for name, plugin in plugins.items():
        plugin.setup(name)

    start_websocket()


def stop():
    for plug in plugins.values():
        plug.cleanup()


def dispatch(ws):
    for name, plugin in plugins.items():
        plugin_data = data.get(name, {})
        plugin.handle(plugin_data, ws)


def on_message(ws, message):
    diff = json.loads(message)
    data.update(diff)

    print(diff)

    dispatch(ws)


def on_error(ws, error):
    print("Error: " + error.message)
    print("Reconnecting...")
    start_websocket()


def on_close(ws):
    print("Connection closed")
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
