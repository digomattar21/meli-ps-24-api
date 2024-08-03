from re import sub

class Route:
    def __init__(self, path, handler, methods=None):
        self.handler = handler
        self.path = path
        self.name = self._getName()
        self.methods = methods or ["GET"]

    def _getName(self):
        return sub(r"\W", "", self.path) or "unknown"
