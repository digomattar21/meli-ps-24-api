from heart.server.controller import BaseController


class HealthCheckController(BaseController):
    
    def get(self, **data):
        return self.send_json({"status": "idle"})