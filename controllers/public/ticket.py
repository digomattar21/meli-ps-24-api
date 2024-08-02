from heart.server.controller import BaseController
from middlemans.ticket import verifyTicketGet


class TicketController(BaseController):
    
    @verifyTicketGet
    def get(self, **data):
        return self.sendJson({"ticket": []})