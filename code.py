from macropad_os import AppRouter, DebugApp
from config import Config

from adafruit_macropad import MacroPad

macropad = MacroPad()
config = Config("config.json")


ar = AppRouter(macropad, config, [
    DebugApp(macropad, config, "DEBUG 1"),
    DebugApp(macropad, config, "DEBUG 2")
])

ar.start()
