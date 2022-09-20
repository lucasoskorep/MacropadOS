from adafruit_hid.keycode import Keycode

class Key(object):
    def __init__(self, name, keycode:Keycodes):
        self.name = name
        self.code = keycode