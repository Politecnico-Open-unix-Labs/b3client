# Simple plugin

class Plugin:
    name = "state"

    def setup(self):
        pass

    def handle(self, data):
        print("---")
        print("State-watcher plugin")
        state = "Open" if data["open"] else "Closed"
        print("Actual state:", state)
        print("---")
        self.send({"asd": 12})

    def clean(self):
        pass
