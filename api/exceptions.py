class MissingRequiredValues(Exception):
    def __init__(self, values: str|list = []) -> None:
        self.values = values
        super().__init__("missing required values")
class TheValueAlreadyExists(Exception):
    def __init__(self, values: str|list = []) -> None:
        self.values = values
        super().__init__("The value already exists")

