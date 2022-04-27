import time

from .app_state import AppState
from .options_app import OptionsApp


class AppRouter(object):
    def __init__(self, macropad, config, apps):
        print("app router")
        self.macropad = macropad
        self.app_index = 0
        self.apps = apps
        self.options = OptionsApp(macropad, config)
        self.current_app = apps[self.app_index]
        self.config = config
        self.encoder_state = False
        self.options_time = 500000000  # .5 seconds in nanoseconds
        self.click_time = 0

    def swap_to_app(self, app):
        """
        TODO: Calculate the size of the stack and the max size of hte stack and then fully close apps if need be.
        :param app:
        :return:
        """
        print("Pausing current app")
        self.current_app.pause()
        print("Selecting new app")
        self.current_app = app
        if self.current_app.state is AppState.STOPPED:
            print("Starting new app")
            self.current_app.start()
        if self.current_app.state is AppState.PAUSED:
            print("Starting new app")
            self.current_app.resume()
        print(time.monotonic_ns())

    def start(self):
        self.current_app.start()
        self.current_app.resume()

        while True:
            # detect if the current app is what should be running
            # stop current app and start new one if not
            self.current_app.loop()
            # any other finite state machine logic that comes up
            if self.macropad.encoder_switch_debounced.pressed and not self.encoder_state:
                self.macropad.play_tone(1000, .1)
                self.encoder_state = True
                self.click_time = time.monotonic_ns()

            elif self.macropad.encoder_switch_debounced.released and self.encoder_state:
                self.encoder_state = False
                if self.current_app is self.options:
                    print("Moving from options to the last opened app.")
                else:
                    self.app_index += 1
                    print("Moving to the next app on the list. ")
                self.swap_to_app(self.apps[self.app_index % len(self.apps)])
                print("released encoder")
            if self.encoder_state and self.click_time:
                self.release_time = time.monotonic_ns()
                if (time.monotonic_ns() - self.click_time) > self.options_time:
                    self.macropad.play_tone(1000, .1)
                    self.swap_to_app(self.options)
                    self.encoder_state = False
            self.macropad.encoder_switch_debounced.update()
