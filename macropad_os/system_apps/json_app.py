import terminalio
import json

from time import monotonic_ns

from adafruit_display_text.bitmap_label import Label
from adafruit_displayio_layout.layouts.grid_layout import GridLayout
from adafruit_hid.keycode import Keycode
from macropad_os import App
from macropad_os.app_utils import rgb_from_int, Macro, MacroSet
from rainbowio import colorwheel

COLOR_UPDATE_RATE = 33000000  # .033 seconds

JSON_FILE_LOCATION = "./macropad_apps/json/"

PROFILE_NAME = "profileName"
SORT_ORDER = "sortOrder"
KEY_KEYS = ["key1", "key2", "key3", "key4", "key5", "key6", "key7", "key8", "key9", "key10", "key11", "key12"]
REQUIRED_KEYS = KEY_KEYS.copy()
REQUIRED_KEYS.extend(x for x in [PROFILE_NAME, SORT_ORDER])


class JsonApp(App):
    def __init__(self, macropad, config, json_file):
        super().__init__(macropad, config)
        self.json_file = json_file
        self.wheel_offset = 0
        self.labels = []
        self.title = ""
        self.last_color_update = 0
        self.active_macro = 0
        self.name = "JSON_APP"
        self.json_dict = JsonApp.read_json_file(self.json_file)
        self.macros = JsonApp.get_macroset_from_dict(self.json_dict)
        self.title = self.json_dict[PROFILE_NAME]
        self.sort_order = self.json_dict[SORT_ORDER]

    @staticmethod
    def create_macro_from_dict(key_dict) -> Macro:
        print(f"Creating macro for {key_dict}")
        name = key_dict["text"]
        values = key_dict["values"]
        codes = []
        for value in values:
            if isinstance(value, str):
                value_mod = 1
                if value[0] is '-':
                    value_mod = -1
                    value = value[1:]
                if hasattr(Keycode, value):
                    keycode = getattr(Keycode, value)
                    codes.append(keycode * value_mod)
                else:
                    codes.append(value)
            if isinstance(value, int) or isinstance(value, float) or isinstance(value, dict) or isinstance(value, list):
                # TODO: Add validation for lists and dictionaries
                codes.append(value)
        print(name, codes)
        return Macro(name, *codes)

    @staticmethod
    def get_macroset_from_dict(json_dict: {}) -> MacroSet:
        key_macros = []
        for key in KEY_KEYS:
            key_macros.append(JsonApp.create_macro_from_dict(json_dict[key]))
        return MacroSet(key_macros=key_macros, encoder_up=Macro("Test"), encoder_down=Macro("Test"))

    @staticmethod
    def read_json_file(json_file) -> {}:
        try:
            f = open(json_file, "r")
            json_dict = json.load(f)
            print(json_dict)
            for key in REQUIRED_KEYS:
                if key not in json_dict:
                    raise ValueError(f"JSON FOR FILE - {json_file} IS INVALID - KEY MISSING {key}")
            return json_dict
        except Exception as e:
            print(e)

    def on_start(self):
        print("on start from the app!")
        self.set_layout(GridLayout(x=0, y=9, width=128, height=54, grid_size=(3, 4), cell_padding=1))
        self.set_title(self.title)
        for i in range(12):
            self.labels.append(
                Label(terminalio.FONT, text=self.macros.get_macro_from_key(i).name))
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
            (r, g, b) = rgb_from_int(colorwheel((pixel / 12 * 256) + self.wheel_offset))
            colors.append((r, g, b))
        self.set_colors(colors)

    def process_keys_pressed_callback(self, key_event):
        print(f"KEY PRESSED - {key_event}")
        print(self.macros)
        macro = self.macros.get_macro_from_key(key_event)
        print(macro)
        print(macro.name)
        print(macro.codes)

        self.press_macro(self.macros.get_macro_from_key(key_event))

    def process_keys_released_callback(self, key_event):
        self.release_macro(self.macros.get_macro_from_key(key_event))

    def process_enbcoder_changed(self, key_event):
        print(key_event)
