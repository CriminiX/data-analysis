class MissingRequiredValues(Exception):
    def __init__(self, values: str|list|None = None) -> None:
        self.values = values
        super().__init__("missing required values")