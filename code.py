import os

from macropad_os import MacropadOS, SerialComms, Config, App

from adafruit_macropad import MacroPad

macropad = MacroPad()

default_config = Config("default_config.json").load()
config = Config("config.json").load(default_config)

PYTHON_APP_FOLDER = "./macropad_apps/python"

apps = []

files = os.listdir(PYTHON_APP_FOLDER)
files.sort()

app_classes = []
for filename in files:
    if filename.endswith('.py') and not filename.startswith('._'):
        try:
            print(filename)
            module = __import__(PYTHON_APP_FOLDER + '/' + filename[:-3])
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

ar = MacropadOS(macropad, config, apps=app_classes)
# sc = SerialComms(config)
# _thread.start_new_thread(sc.run, (sc))
ar.start()
