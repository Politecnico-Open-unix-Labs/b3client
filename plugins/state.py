# Simple plugin


def setup(name):
    pass


def handle(data, ws):
    print("---")
    print("State-watcher plugin")
    state = "Open" if data["open"] else "Closed"
    print("Actual state:", state)
    print("---")


def clean():
    pass
