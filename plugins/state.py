# Simple plugin


def setup(name, ws):
    pass


def handle(data):
    print("---")
    print("State-watcher plugin")
    state = "Open" if data["open"] else "Closed"
    print("Actual state:", state)
    print("---")


def clean():
    pass
