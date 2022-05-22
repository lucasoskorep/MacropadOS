import time


class SerialComms(object):
    def __init__(self, config):
        self.config = config

    def loop(self):
        print("Hello")

    def run(self):
        while True:
            self.loop()
            time.sleep(.5)


