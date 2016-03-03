import json
import time
import logging
from threading import Thread
from websocket import WebSocketApp

log_level = "error"
log_file = "/tmp/b3d.log"

# Inizialize logging
log_level = getattr(logging, log_level.upper(), None)

logging.basicConfig(level=log_level)
log = logging.getLogger(__name__)

log_fd = logging.FileHandler(log_file, "w")
log_fd.setLevel(log_level)
log.addHandler(log_fd)
#


class Client(object):
    def __init__(self, server, token=""):
        self.server = server
        self.token = token
        self.data = {}
        self.ws = None

    def send(self, msg):
        "Send msg (a dict) to the server"

        if not self.ws:
            return

        self.ws.send(json.dumps(dict(msg, **{"key": self.token})))

    def start(self):
        log.info("Starting websocket")
        self.ws = WebSocketApp(self.server, [],
                               self.cb_on_open, self.cb_on_message,
                               self.cb_on_error, self.cb_on_close)

        self.ws.run_forever()

    def on_message(self, f):
        def cb(ws, message):
            f(message)
        self.cb_on_message = cb

    def cb_on_message(self, ws, message):
        pass

    def cb_on_error(self, ws, error):
        "Restart websocket"
        log.error("Error: %s", error)
        time.sleep(1)
        log.info("Reconnecting...")
        self.start()

    def cb_on_close(self, ws):
        "On connection close, cleanup things"
        log.info("Connection closed")

    def cb_on_open(self, ws):
        "Send empty jsons to keep alive the connection, on an separate thread"
        def channel():
            while True:
                ws.send("{}")  # ping to avoid timeout
                time.sleep(15)

        Thread(target=channel).start()
