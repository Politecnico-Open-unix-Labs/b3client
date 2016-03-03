import json
import re
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


def parse_path(path):
    "Split path in a list"
    return re.findall(r"[\w]+", path)


def set_value(d, path, value):
    "Set value in a dictonary given the path"
    path = parse_path(path)

    if not path:
        return

    while len(path) > 1:
        d[path[0]] = {}

        d = d[path[0]]
        path = path[1:]

    d[path[0]] = value


def get_value(d, path):
    "Get value from a dictonary given the path"
    path = parse_path(path)

    if not path:
        return {}

    while len(path) > 1:
        key = path[0]
        if key in d:
            d = d[key]
        else:
            return {}
        path = path[1:]

    key = path[0]
    if key in d:
        return d[key]
    else:
        return {}


class Client(object):
    def __init__(self, server, token=""):
        "Initialize"
        self.server = server
        self.token = token
        self.callbacks = {}
        self.ws = None

    def send(self, path, value):
        "Send msg (a dict) to the server"
        msg = {"key": self.token}
        set_value(msg, path, value)

        if not self.ws:
            return

        self.ws.send(json.dumps(msg))

    def start(self):
        "Start websocket"
        log.info("Starting websocket")
        self.ws = WebSocketApp(self.server, [],
                               self.cb_on_open, self.cb_on_message,
                               self.cb_on_error, self.cb_on_close)

        self.ws.run_forever()

    def on_message(self, path):
        "Decore a funcion to make it a callback"
        def decorator(f):
            self.callbacks[path] = f

        return decorator

    def cb_on_message(self, ws, message):
        "Dispatch messages to callbacks"
        for path in self.callbacks:
            value = get_value(json.loads(message),
                              path)

            if value != {}:
                self.callbacks[path](value)

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
