import json

from .config_item import ConfigItem


class Config(object):
    def __init__(self, save_file):
        self._data = {}
        self._items = {}
        self._save_file = save_file

    def load(self, default_config=None):
        try:
            f = open(self._save_file, "r")
            self._data = json.load(f)
            self._items = {}
            for key, value in self._data.items():
                self._items[key] = ConfigItem.from_json(key, value)
        except Exception as e:
            print(e)
            self._items = {}
            self._data = {}
        if default_config:
            for item in default_config._items:
                if not (item in self._items):
                    self._items[item] = default_config._items[item]
        return self

    def get_items(self):
        return self._items

    def get_item_by_name(self, key):
        if key in self._items:
            return self._items[key]
        else:
            return None

    def set_item(self, config_item: ConfigItem):
        self._items[config_item.name] = config_item
        return self

    def save(self):
        save_format = {}
        for name, item in self._items.items():
            save_format[name] = item.to_json()
        with open(self._save_file, "w") as f:
            json.dump(save_format, f)
            self._data = save_format
        return self

    def key_tone_enabled(self):
        return self.get_item_by_name("key_tone").value

    def key_tone_hz(self):
        return self.get_item_by_name("key_tone_hz").value if self.key_tone_enabled() else 0

    def brightness(self):
        return self.get_item_by_name("brightness").value

    def debug_app_enabled(self):
        return self.get_item_by_name("debug_app").value