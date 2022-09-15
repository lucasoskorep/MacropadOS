from macropad_os import AppRouter, SerialComms, Config

from adafruit_macropad import MacroPad

from macropad_apps.python import NumpadApp

macropad = MacroPad()

default_config = Config("default_config.json").load()
config = Config("config.json").load(default_config)

ar = AppRouter(macropad, config, [
    NumpadApp(macropad, config),
#  Arrow Keys
#  Script Runner
])

sc = SerialComms(config)

# _thread.start_new_thread(sc.run, (sc))

ar.start()
