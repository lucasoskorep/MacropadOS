import storage

from macropad_os import Config


default_config = Config("default_config.json").load()
config = Config("config.json").load(default_config)
dev_mode = config.get_item_by_name("dev_mode")

if dev_mode :
    if not dev_mode.value:
        print("file system should not be writable - dev mode not active")
        storage.disable_usb_drive()
        storage.remount("/", False)
        dev_mode_active = config.get_item_by_name("dev_mode_active")
        dev_mode_active.value = False
        config.set_item(dev_mode_active)
        config.save()
    else:
        # dev mode is on and needs to be disabled
        print("Disabling dev mode before boot so that settings will work")
        storage.disable_usb_drive()
        storage.remount("/", False)
        dev_mode = config.get_item_by_name("dev_mode")
        dev_mode.value = False
        config.set_item(dev_mode)
        dev_mode_active = config.get_item_by_name("dev_mode_active")
        dev_mode_active.value = True
        config.set_item(dev_mode_active)
        config.save()
        storage.enable_usb_drive()
        storage.remount("/", True)