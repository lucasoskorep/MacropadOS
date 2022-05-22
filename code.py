from macropad_os import AppRouter, DebugApp, SerialComms
from macropad_os.config import Config

from adafruit_macropad import MacroPad


macropad = MacroPad()
config = Config("config.json")


ar = AppRouter(macropad, config, [
    DebugApp(macropad, config, "DEBUG 1"),
    DebugApp(macropad, config, "DEBUG 2")
])

sc = SerialComms(config)

# _thread.start_new_thread(sc.run, (sc))

ar.start()
