from heart.server.controller import BaseController
from gateways.ticket import TicketGateway
from gateways.category import CategoryGateway
from gateways.severity import SeverityGateway
from middlemans.ticket import verifyTicketGet, verifyTicketCreate
from utils.apiMessages import errorMessage, LocalApiCode
class TicketController(BaseController):
    
    @verifyTicketGet
    def get(self, **data):
        ticket_id = data.get('id')
        if ticket_id:
            ticket = TicketGateway.get_by_id(ticket_id)
            if ticket:
                return self.sendJson({"ticket": ticket.to_dict()})
            return self.sendJson({"errors": [errorMessage(LocalApiCode.ticketNotFound)]})
        
        tickets = TicketGateway.get_all()
        return self.sendJson({"tickets": [ticket.to_dict() for ticket in tickets]})

    @verifyTicketCreate
    def post(self, **data):
        title = data.get('title')
        description = data.get('description')
        category_id = data.get('category_id')
        subcategory_id = data.get('subcategory_id')
        severity_level = data.get('severity')

        severity = SeverityGateway.get_by_level(severity_level)
        if severity_level == 1:
            return self.sendJson({"errors": [errorMessage(LocalApiCode.invalidSeverity)]})
        
        category = CategoryGateway.get_by_id(category_id)
        if not category:
            return self.sendJson({"errors": [errorMessage(LocalApiCode.invalidCategory)]})
        
        subcategory = CategoryGateway.get_by_id(subcategory_id)
        if not subcategory or subcategory.parent_id != category_id:
            return self.sendJson({"errors": [errorMessage(LocalApiCode.invalidSubcategory)]})
        
        new_ticket = TicketGateway.create(
            title=title,
            description=description,
            category_id=category_id,
            subcategory_id=subcategory_id,
            severity_id=severity.id
        )
        ticket_id = TicketGateway.save(new_ticket)
        return self.sendJson({"ticket_id": ticket_id}, 201)

    # @verifyTicketUpdate
    def patch(self, **data):
        ticket_id = data.get('id')
        ticket = TicketGateway.get_by_id(ticket_id)
        if not ticket:
            return self.sendJson({"errors": [errorMessage(LocalApiCode.ticketNotFound)]})
        
        updated_ticket = TicketGateway.update(ticket_id, **data)
        if updated_ticket:
            return self.sendJson({"ticket": updated_ticket.to_dict()})
        
        return self.sendJson({"errors": [errorMessage(LocalApiCode.internalError)]})

    # @verifyTicketDelete
    def delete(self, **data):
        ticket_id = data.get('id')
        ticket = TicketGateway.get_by_id(ticket_id)
        if not ticket:
            return self.sendJson({"errors": [errorMessage(LocalApiCode.ticketNotFound)]})
        
        TicketGateway.delete(ticket_id)
        return self.sendJson({"message": "Ticket deleted successfully"})
