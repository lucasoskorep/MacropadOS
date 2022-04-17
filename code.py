import displayio

from app import AppRouter, DebugApp
from config import Config
from adafruit_macropad import MacroPad

macropad = MacroPad()
config = Config("config.json")


ar = AppRouter(macropad, config, [
    DebugApp(macropad, config, "debug 1"),
    # DebugApp(macropad, config, "debug 2"),
    # DebugApp(macropad, config, "debug 3")
])

ar.start()
