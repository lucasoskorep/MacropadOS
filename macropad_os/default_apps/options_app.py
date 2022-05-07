from adafruit_displayio_layout.layouts.grid_layout import GridLayout

from .common import arrows_yes_no, arrows_with_enter, up_down_enter
from ..abstract_app import App


class OptionsApp(App):

    def __init__(self, macropad, config):
        super().__init__(macropad, config)
        self.send_keyboard_inputs = 0
        self.labels = []
        self.key_colors = arrows_yes_no
        self.possible_key_colors = [arrows_yes_no, arrows_with_enter, up_down_enter]
        self.counter = 0
        self.title = "Options"

    def on_start(self):
        print("on start from the options app!")
        self.set_title(self.title)
        self.set_layout(GridLayout(x=0, y=9, width=128, height=54, grid_size=(4, 4), cell_padding=1))

    def on_resume(self):
        print("resume from the options app!")

    def on_pause(self):
        print("Pausing")


    def on_stop(self):
        print("Stopping")

    def on_loop(self):
        pass

    def on_key_pressed(self, keyevent):
        print("ON KEY PRESSED CALLBACK FROM OPTIONS")
        print(keyevent)

    def on_key_released(self, keyevent):
        print("ON KEY RELEASED CALLBACK FROM OPTIONS")
        print(keyevent)

    def on_wheel_change(self, event):
        print("ON WHEEL CHANGED CALLBACK")
        print(event)



