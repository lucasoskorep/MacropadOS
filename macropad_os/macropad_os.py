import time, os

from . import App
from .app_state import AppState

from macropad_os.system_apps import OptionsApp, DebugApp, JsonApp


class MacropadOS(object):
    def __init__(self, macropad, config, python_apps: str, json_apps: str):
        print("app router")
        self.macropad = macropad
        self.app_index = 0
        self.options = OptionsApp(macropad, config)
        self.config = config
        self.encoder_state = False
        self.options_time = 500000000  # .5 seconds in nanoseconds
        self.click_time = 0
        self.debug_app = DebugApp(macropad, config, "DEBUG APP")
        self.debug_app_active = self.config.debug_app_enabled()
        self.python_apps_location = python_apps
        self.json_apps_location = json_apps
        self.apps: [App] = []
        self.load_python_apps()
        self.load_json_apps()
        self.current_app = self.apps[self.app_index]
        if self.debug_app_active:
            self.apps.append(self.debug_app)

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
        if self.current_app._state is AppState.STOPPED:
            print("Starting new app")
            self.current_app.start()
        if self.current_app._state is AppState.PAUSED:
            print("Starting new app")
            self.current_app.resume()

    def load_python_apps(self):
        app_classes = []
        for filename in sorted(os.listdir(self.python_apps_location)):
            if filename.endswith('.py') and not filename.startswith('._'):
                try:
                    print(filename)
                    module = __import__(self.python_apps_location + '/' + filename[:-3])
                    classes = [getattr(module, a) for a in dir(module)
                               if isinstance(getattr(module, a), type)]
                    for cls in classes:
                        if issubclass(cls, App) and cls.__name__ != "App":
                            app_classes.append(cls)
                    print(app_classes)
                except (SyntaxError, ImportError, AttributeError, KeyError, NameError, IndexError, TypeError) as err:
                    print("ERROR in", filename)
                    import traceback
                    traceback.print_exception(err, err, err.__traceback__)
        self.apps.extend(a(self.macropad, self.config) for a in app_classes)

    def load_json_apps(self):
        json_apps = []
        for filename in sorted(os.listdir(self.json_apps_location)):
            if filename.endswith('.json'):
                json_apps.append(
                    JsonApp(
                        self.macropad,
                        self.config,
                        self.json_apps_location + "/" + filename
                    )
                )
        json_apps.sort(key=lambda x: x.sort_order)
        self.apps.extend(json_apps)

    def start(self) -> None:
        print(self.current_app)
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
                    if self.debug_app_active != self.config.debug_app_enabled():
                        if self.debug_app_active:
                            self.apps.append(self.debug_app)
                        else:
                            self.apps.remove(self.debug_app)
                        self.debug_app_active = self.config.debug_app_enabled()
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
