import terminalio
from adafruit_display_text import bitmap_label as label
from adafruit_displayio_layout.layouts.grid_layout import GridLayout
from rainbowio import colorwheel

from .abstract_app import App


def rgb_from_int(rgb):
    blue = rgb & 255
    green = (rgb >> 8) & 255
    red = (rgb >> 16) & 255
    return red, green, blue


class DebugApp(App):

    def __init__(self, macropad, config, name):
        super().__init__(macropad, config)
        self.name = name
        self.tones = [196, 220, 246, 262, 294, 330, 349, 392, 440, 494, 523, 587]
        self.wheel_offset = 0
        self.send_keyboard_inputs = 0
        self.lit_keys = [False] * 12
        self.labels = []
        self.layout = GridLayout(x=0, y=9, width=128, height=54, grid_size=(4, 4), cell_padding=1)
        self.title = label.Label(
            y=4,
            font=terminalio.FONT,
            color=0x0,
            text=f"     {self.name} MENU     ",
            background_color=0xFFFFFF,
        )

    def on_start(self):
        print("on start from the app!")
        self.lit_keys = [False] * 12
        self.macropad.display.show(self.display_group)
        for _ in range(12):
            self.labels.append(label.Label(terminalio.FONT, text=""))

        for index in range(12):
            x = index % 3
            y = index // 3
            self.layout.add_content(self.labels[index], grid_position=(x, y), cell_size=(1, 1))


    def on_resume(self):
        print("resume from the debug app!")

        print(id(self.display_group))
        print(self.display_group)
        self.display_group.append(self.title)
        self.display_group.append(self.layout)
        self.macropad.display.show(self.display_group)

    def on_pause(self):
        print("Pausing")

        self.display_group.remove(self.title)
        self.display_group.remove(self.layout)
        # self.macropad.display.show(None)


    def on_stop(self):
        print("Stopping")

    def loop(self):
        self.process_key_presses()
        self.light_keys()

    def process_key_presses(self):
        key_event = self.macropad.keys.events.get()
        if key_event:
            if key_event.pressed:
                self.labels[key_event.key_number].text = "KEY{}".format(key_event.key_number)
                print(self.macropad.keys)
                self.lit_keys[key_event.key_number] = not self.lit_keys[key_event.key_number]
                self.macropad.stop_tone()
                self.macropad.start_tone(self.tones[key_event.key_number])
            else:
                self.labels[key_event.key_number].text = ""
                self.macropad.stop_tone()

    def light_keys(self):
        self.wheel_offset += 1
        for pixel in range(12):
            if self.lit_keys[pixel]:
                (r, g, b) = rgb_from_int(colorwheel((pixel / 12 * 256) + self.wheel_offset))
                self.macropad.pixels[pixel] = (r * .1, g * .1, b * .1)
            else:
                self.macropad.pixels[pixel] = 0
