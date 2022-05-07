import displayio
import terminalio
from adafruit_display_text import label
from adafruit_hid.keycode import Keycode

from .app_state import AppState, InvalidStateUpdateError

DISPLAY = displayio.Group()


def convert_to_keynum(x, y):
    return 3 * x + y


class App(object):

    def __init__(self, macropad, config):
        """

        :param macropad:
        :param config:
        """
        print("app created")
        self._key_lights = [(0, 0, 0) for _ in range(12)]
        self._display_group = DISPLAY
        self._title = "title"
        self._layout = None
        self._title_label = label.Label(
            y=4,
            font=terminalio.FONT,
            color=0x0,
            text=f"",
            background_color=0xFFFFFF,
        )
        self._key_tones = [config.data["default_tone"] for _ in range(12)]
        self._enabled_key_sounds = True
        self._pressed_keys = []
        self._key_pressed_callbacks = []
        self._key_released_callbacks = []
        self._encoder_changed_callbacks = []
        self._encoder_state = 0


        self.macropad = macropad
        self.config = config
        self.name = "app"
        self.state = AppState.STOPPED

    def start(self):
        print("Start from base class ")
        if self.state is not AppState.STOPPED:
            raise InvalidStateUpdateError(f"Start called but the current app state is {self.state}")
        self.state = AppState.STARTING
        self._on_start()
        self.on_start()
        self.state = AppState.PAUSED

    def _on_start(self):
        pass

    def on_start(self):
        raise NotImplementedError("on_start not implemented")

    def resume(self):
        if self.state is not AppState.PAUSED:
            raise InvalidStateUpdateError(f"Resume called but the current app state is {self.state}")
        self.state = AppState.RESUMING
        self._on_resume()
        self.on_resume()
        self.state = AppState.RUNNING

    def _on_resume(self):
        self.add_displays_to_group()

    def on_resume(self):
        raise NotImplementedError("on_resume not implemented")

    def pause(self):
        if self.state is not AppState.RUNNING:
            raise InvalidStateUpdateError(f"Pause called but the current app state is {self.state}")
        self.state = AppState.PAUSING
        self._on_pause()
        self.on_pause()
        self.state = AppState.PAUSED

    def _on_pause(self):
        self.macropad.keyboard.release_all()
        self.macropad.consumer_control.release()
        self.macropad.mouse.release_all()
        self.macropad.stop_tone()
        self.macropad.pixels.show()
        self.remove_displays_from_group()

    def on_pause(self):
        raise NotImplementedError("on_pause not implemented")

    def loop(self):
        # We'll fire you if you override this method.
        self._on_loop()
        self.on_loop()

    def on_loop(self):
        raise NotImplementedError("Not implemented")

    def _on_loop(self):
        self._update_lighting()
        self._process_keys_pressed()
        self._process_wheel_changes()
        self.on_loop()

    def _process_keys_pressed(self):
        key_event = self.macropad.keys.events.get()
        if key_event:
            if key_event.key_number < 12:
                if key_event.pressed:
                    self.macropad.stop_tone()
                    self.macropad.start_tone(self._key_tones[key_event.key_number])
                    self._pressed_keys.append(key_event.key_number)
                    if self._key_pressed_callbacks:
                        for callback in self._key_pressed_callbacks:
                            callback(key_event.key_number)
                else:
                    self.macropad.stop_tone()
                    self._pressed_keys.remove(key_event.key_number)
                    if self._pressed_keys:
                        self.macropad.start_tone(self._key_tones[self._pressed_keys[0]])
                    if self._key_released_callbacks:
                        for callback in self._key_pressed_callbacks:
                            callback(key_event.key_number)

    def _process_wheel_changes(self):
        encoder = self.macropad.encoder
        if self._encoder_state != encoder:
            for callback in self._encoder_changed_callbacks:
                if self._encoder_state > encoder:
                    callback(-1)
                else:
                    callback(1)
            self._encoder_state = encoder

    def stop(self):
        if self.state is not AppState.PAUSED:
            raise InvalidStateUpdateError(f"Stop called but the current app state is {self.state}")
        self.state = AppState.STOPPING
        self._on_stop()
        self.on_stop()
        self.state = AppState.STOPPED

    def _on_stop(self):
        pass

    def on_stop(self):
        raise NotImplementedError("on_stop not implemented.")

    def _update_lighting(self):
        for index, color in enumerate(self._key_lights):
            self.macropad.pixels[index] = color

    def add_displays_to_group(self):
        self._display_group.append(self._title_label)
        self._display_group.append(self._layout)
        self.macropad.display.show(self._display_group)

    def remove_displays_from_group(self):
        self._display_group.remove(self._title_label)
        self._display_group.remove(self._layout)

    def set_color(self, x, y, color):
        key_value = convert_to_keynum(x, y)
        if key_value >= 12:
            raise ValueError("color index out of range")
        if len(color) != 3:
            self._key_lights[key_value] = color

    def set_colors(self, colors):
        if len(colors) != 12:
            raise ValueError("Colors must be passed in as a 12 len array")
        for color in colors:
            if len(color) != 3:
                raise ValueError("Color format error - color must be length 3")
        self._key_lights = colors

    def get_colors(self):
        return self._key_lights

    def set_tone(self, keypad_num, tone):
        if keypad_num >= 12:
            raise ValueError("Tone index out of range")
        if tone < 20 or tone > 20000:
            raise ValueError("Tone format error - tone out of human hearing range (20 - 20000)")
        self._key_tones[keypad_num] = tone

    def set_tones(self, tones):
        if len(tones) != 12:
            raise ValueError("Tones must be passed in as a 12 len array")
        for tone in tones:
            if tone < 20 or tone > 20000:
                raise ValueError("Tone format error - tone out of human hearing range (20 - 20000)")
        self._key_tones = tones

    def set_tone_status(self, enable):
        self._enabled_key_sounds = enable

    def get_tones(self):
        return self._key_tones

    def set_title(self, title):
        """
        :string title: Title of your app - shown in the top bar.

        :return: None
        """
        if len(title) > 22:
            # TODO: Update this to be able to scroll the display if too long?
            raise ValueError("Title too long to be displayed on screen")
        self._title = title
        diff = int((22 - len(title)) / 2)
        self._title_label.text = f"{''.join([' ' for _ in range(diff)])}{self._title}{''.join([' ' for _ in range(diff)])}"

    def set_layout(self, layout):
        """
        :displayio.Group layout:

        :return:
        """
        self._layout = layout

    def register_on_key_pressed(self, function):
        self._key_pressed_callbacks.append(function)

    def register_on_key_released(self, function):
        self._key_released_callbacks.append(function)

    def register_on_encoder_changed(self, function):
        self._encoder_changed_callbacks.append(function)


