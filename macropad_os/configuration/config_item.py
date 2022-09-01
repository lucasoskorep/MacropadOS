class ValueRange(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end

    @staticmethod
    def from_json(json_dict: dict):
        if not ("start" in json_dict and "end" in json_dict):
            raise ValueError("Value Range must be provided a start and end value in the provided json dictionary")
        return ValueRange(json_dict["start"], json_dict["end"])

    def to_json(self):
        return {
            "start": self.start,
            "end": self.end
        }

    def __str__(self):
        return f"{self.to_json()}"


class ConfigItem(object):
    def __init__(self, name: str, value, available_values: list = None, value_range: ValueRange = None,
                 dependency: dict = None):
        self.name = name
        self.value = value
        self.available_values = available_values
        self.value_range = value_range
        self.dependency = dependency

    @staticmethod
    def from_json(key: str, json_dict: dict):
        return ConfigItem(
            key,
            json_dict["current_value"],
            available_values=json_dict["available_values"] if "available_values" in json_dict else None,
            value_range=ValueRange.from_json(json_dict["value_range"]) if "value_range" in json_dict else None,
            dependency=json_dict["dependency"] if "dependency" in json_dict else None,
        )

    def to_json(self):
        json_dict = {"current_value": self.value}
        if self.value_range:
            json_dict["value_range"] = self.value_range.to_json()
        if self.available_values:
            json_dict["available_values"] = self.available_values
        if self.dependency:
            json_dict["dependency"] = self.dependency

        return json_dict
