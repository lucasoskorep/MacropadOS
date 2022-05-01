import terminalio
from adafruit_display_text import label
from adafruit_displayio_layout.layouts.grid_layout import GridLayout

from .common import arrows_yes_no, arrows_with_enter, up_down_enter
from ..abstract_app import App


class OptionsApp(App):

    def __init__(self, macropad, config):
        super().__init__(macropad, config)
        self.send_keyboard_inputs = 0
        self.labels = []
        self.layout = GridLayout(x=0, y=9, width=128, height=54, grid_size=(4, 4), cell_padding=1)
        self.key_colors = arrows_yes_no
        self.possible_key_colors = [arrows_yes_no, arrows_with_enter, up_down_enter]
        self.title = label.Label(
            y=4,
            font=terminalio.FONT,
            color=0x0,
            text=f"     OPTIONS MENU     ",
            background_color=0xFFFFFF,
        )
        self.counter = 0

    def on_start(self):
        print("on start from the app!")
        self.lit_keys = [False] * 4
        for _ in range(4):
            self.labels.append(label.Label(terminalio.FONT, text=""))

        for index in range(4):
            x = 0
            y = index
            self.layout.add_content(self.labels[index], grid_position=(x, y), cell_size=(3, 1))

    def on_resume(self):
        print("resume from the options app!")
        self.display_group.append(self.title)
        self.display_group.append(self.layout)
        self.macropad.display.show(self.display_group)

    def on_pause(self):
        print("Pausing")
        self.display_group.remove(self.title)
        self.display_group.remove(self.layout)

    def on_stop(self):
        print("Stopping")

    def loop(self):
        self.process_key_presses()
        self.light_keys()
        self.key_colors = self.possible_key_colors[self.counter % len(self.possible_key_colors)]
        self.counter+=1

    def process_key_presses(self):
        key_event = self.macropad.keys.events.get()
        if key_event:
            if key_event.key_number < 12:
                if key_event.pressed:
                    self.macropad.stop_tone()
                    self.macropad.start_tone(440)
                else:
                    self.macropad.stop_tone()

    def light_keys(self):
        for pixel in range(12):
            self.macropad.pixels[pixel] = self.key_colors[pixel]
