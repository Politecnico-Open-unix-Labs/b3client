#!/usr/bin/env python3
import websocket
import json
import time
from threading import Thread

data = {}


def on_message(ws, message):
    diff = json.loads(message)
    data.update(diff)

    print(diff)

    # TODO dispatching


def on_error(ws, error):
    print("Error: " + error.message)
    print("Reconnecting...")
    start_websocket()


def on_close(ws):
    print("Connection closed")


def on_open(ws):
    def ping():
        # ws.recv()
        ws.send(json.dumps({"test": 123, "key": "antani"}))
        while 1:
            # TODO
            # plugin handling, passing them data
            # and running them in an other thread
            ws.send("{}")
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
    start_websocket()
