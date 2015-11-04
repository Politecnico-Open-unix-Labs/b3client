# Simple plugin

class Plugin:
    def setup(self, name, send):
        self.send = send

    def handle(self, data):
        print("---")
        print("State-watcher plugin")
        state = "Open" if data["open"] else "Closed"
        print("Actual state:", state)
        print("---")
        self.send({"asd": 12})

    def clean(self):
        pass
