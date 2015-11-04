# Simple plugin

send = None


def setup(name, _send):
    global send
    send = _send
    pass


def handle(data):
    print("---")
    print("State-watcher plugin")
    state = "Open" if data["open"] else "Closed"
    print("Actual state:", state)
    print("---")
    send({"asd": 12})


def clean():
    pass
