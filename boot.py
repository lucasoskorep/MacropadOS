import storage

from config import Config, ConfigVars

config = Config("config.json")

print("test")
print(config.data)

if not config.data.get(ConfigVars.DEV_MODE.name):
    storage.disable_usb_drive()
    print("file system should be writable")
    storage.remount("/", False)
    config.data[ConfigVars.DEV_MODE.name] = True
    config.save()
    print("success")
