# import RPi.GPIO as GPIO

class Plugin:
    section = "state"

    def setup(self):
        # GPIO.setmode(GPIO.BOARD)
        # GPIO.setup(led, GPIO.OUT)
        # GPIO.output(led, GPIO.HIGH)  # red
        # GPIO.output(led, GPIO.LOW)  # green
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
