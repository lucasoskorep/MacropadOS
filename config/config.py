import json

from .config_vars import ConfigVars


class Config(object):
    def __init__(self, save_file):
        self.data = {}
        self.save_file = save_file
        self.load()

    def load(self):
        with open(self.save_file, "r") as f:
            self.data = json.load(f)
            for convar in ConfigVars.__dict__.keys():
                print(convar)

    def save(self):
        with open(self.save_file, "w") as f:
            json.dump(self.data, f)

