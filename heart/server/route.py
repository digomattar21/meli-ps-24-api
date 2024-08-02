from re import sub


class Route:

    def __init__(self, path, handler):
        self.handler = handler
        self.path = path
        self.name = self._getName()

    def _getName(self):
        return sub(r"\W", "", self.path) or "unknown"
