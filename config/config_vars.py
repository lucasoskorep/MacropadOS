class ConVar(object):
    def __init__(self, name, default):
        self.name = name
        self.default = default


class ConfigVars(object):
    DEV_MODE = ConVar("dev_mode", True)
    TEST_VAR = ConVar("test_var", False)
