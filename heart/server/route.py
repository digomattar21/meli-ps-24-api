from re import sub

class Route:
    def __init__(self, path, handler, methods=None):
        self.handler = handler
        self.path = path
        self.name = self._get_name()
        self.methods = methods or ["GET"]

    def _get_name(self):
        return sub(r"\W", "", self.path) or "unknown"
