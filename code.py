import os

from macropad_os import MacropadOS, SerialComms, Config, App

from adafruit_macropad import MacroPad

macropad = MacroPad()

default_config = Config("default_config.json").load()
config = Config("config.json").load(default_config)

PYTHON_APP_FOLDER = "./macropad_apps/python"
JSON_APP_FOLDER = "./macropad_apps/json"

ar = MacropadOS(
    macropad,
    config,
    python_apps=PYTHON_APP_FOLDER,
    json_apps=JSON_APP_FOLDER
)
# sc = SerialComms(config)
# _thread.start_new_thread(sc.run, (sc))
ar.start()
