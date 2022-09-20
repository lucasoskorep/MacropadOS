from time import monotonic_ns

import terminalio
from adafruit_display_text.bitmap_label import Label

from adafruit_displayio_layout.layouts.grid_layout import GridLayout
from adafruit_hid.keycode import Keycode
from rainbowio import colorwheel

from macropad_os import App
from macropad_os.app_utils import rgb_from_int


labels = [
    "7", "8", "9",
    "4", "5", "6",
    "1", "2", "3",
    "0", ".", "SHIFT"
]

modified_labels = [
    "<", ">", "&",
    "(", ")", "%",
    "/", "+", "-",
    "*", "=", "SHIFT"
]


COLOR_UPDATE_RATE = 33000000 # .033 seconds

class NumpadApp(App):

    def __init__(self, macropad, config):
        super().__init__(macropad, config)
        self.name = "Numpad"
        self.wheel_offset = 0
        self.lit_keys = [False] * 12
        self.labels = []
        self.title = "Numpad"
        self.modifier_pressed = False
        self.last_color_update = 0

    def on_start(self):
        print("on start from the app!")
        self.set_layout(GridLayout(x=0, y=9, width=128, height=54, grid_size=(3, 4), cell_padding=1))
        self.set_title(self.title)
        self.lit_keys = [True] * 12
        for i in range(12):
            self.labels.append(Label(terminalio.FONT, text=labels[i]))
        for index in range(12):
            x = index % 3
            y = index // 3
            self._layout.add_content(self.labels[index], grid_position=(x, y), cell_size=(1, 1))
        self.register_on_key_pressed(self.process_keys_pressed_callback)
        self.register_on_key_released(self.process_keys_released_callback)
        self.register_on_encoder_changed(self.process_enbcoder_changed)

    def on_resume(self):
        print("resume from the debug app!")

    def on_pause(self):
        print("Pausing")

    def on_stop(self):
        print("Stopping")

    def on_loop(self):
        self.update_key_colors()

    def update_key_colors(self):
        self.wheel_offset += 1
        colors = []

        last_update_ago = monotonic_ns() - self.last_color_update
        if last_update_ago > COLOR_UPDATE_RATE:
            self.last_color_update = monotonic_ns()
        for pixel in range(12):
            if self.lit_keys[pixel]:
                (r, g, b) = rgb_from_int(colorwheel((pixel / 12 * 256) + self.wheel_offset))
                colors.append((r, g, b))
            else:
                colors.append((0, 0, 0))
        self.set_colors(colors)

    def process_keys_pressed_callback(self, keyevent):
        print(keyevent)
        self.keyboard.send(Keycode.SHIFT,Keycode.SHIFT,Keycode.SHIFT, Keycode.A)

    def process_keys_released_callback(self, keyevent):
        print(keyevent)

    def process_enbcoder_changed(self, keyevent):
        print(keyevent)