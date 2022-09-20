class Macro(object):
    def __init__(self, name, *codes, released = None):
        self.name = name
        self.codes = codes
        self.released = released


class MacroSet(object):
    def __init__(self, key_macros: [Macro], encoder_up: Macro, encoder_down: Macro):
        if len(key_macros) != 12:
            raise ValueError("12 keys must be passed to a keyset")
        self._key_macros = key_macros
        self.encoder_up = encoder_up
        self.encoder_down = encoder_down

    def get_macro_from_key(self, key_index) -> Macro:
        if key_index < 0 or key_index > 11:
            raise ValueError("Invalid key index")
        return self._key_macros[key_index]

