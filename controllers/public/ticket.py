from heart.server.controller import BaseController
from gateways.ticket import TicketGateway
from gateways.category import CategoryGateway
from gateways.severity import SeverityGateway
from middlemans.ticket import verifyTicketGet, verifyTicketPost, verifyTicketPatch, verifyTicketDelete
from utils.apiMessages import errorMessage, LocalApiCode
class TicketController(BaseController):
    
    @verifyTicketGet
    def get(self, ticket_id=None, **data):
        if ticket_id:
            ticket = TicketGateway.get_by_id(ticket_id)
            if ticket:
                return self.sendJson({"ticket": ticket.to_dict()})
            return self.sendJson({"errors": [errorMessage(LocalApiCode.ticketNotFound)]})
        
        tickets = TicketGateway.get_all()
        return self.sendJson({"tickets": [ticket.to_dict() for ticket in tickets]})

    @verifyTicketPost
    def post(self, **data):
        title = data.get('title')
        description = data.get('description')
        category_id = data.get('category_id')
        subcategory_id = data.get('subcategory_id')
        severity_level = data.get('severity')

        new_ticket = TicketGateway.create(
            title=title,
            description=description,
            category_id=category_id,
            subcategory_id=subcategory_id,
            severity_id=severity_level
        )

        return self.sendJson({"ticket": new_ticket.to_dict()})

    @verifyTicketPatch
    def patch(self, ticket_id, **data):
        updated_ticket = TicketGateway.update(ticket_id, **data)
        if updated_ticket:
            return self.sendJson({"ticket": updated_ticket.to_dict()})
        
        return self.sendJson({"errors": [errorMessage(LocalApiCode.internalError)]})

    @verifyTicketDelete
    def delete(self, ticket_id):
        TicketGateway.delete(ticket_id)
        return self.sendJson({"message": "Ticket deleted successfully"})
