from heart.server.controller import BaseController
from middlemans.ticket import (
    verify_ticket_exists,
    verify_ticket_get,
    verify_ticket_patch,
    verify_ticket_post,
)
from services.ticket import TicketService


class TicketController(BaseController):

    @verify_ticket_get
    def get(self, ticket_id=None):
        if ticket_id:
            ticket_data = TicketService.get_ticket_by_id(ticket_id)
            if "errors" in ticket_data:
                return self.send_json(ticket_data)
            return self.send_json(ticket_data)

        result = TicketService.get_all_tickets()
        return self.send_json(result)

    @verify_ticket_post
    def post(self, **data):
        result = TicketService.create_ticket(
            title=data.get("title"),
            description=data.get("description"),
            category_id=data.get("category_id"),
            subcategory_id=data.get("subcategory_id"),
            severity_id=data.get("severity_id"),
        )
        return self.send_json(result)

    @verify_ticket_exists
    @verify_ticket_patch
    def patch(self, ticket_id, **data):
        result = TicketService.update_ticket(ticket_id, **data)
        return self.send_json(result)

    @verify_ticket_exists
    def delete(self, ticket_id):
        result = TicketService.delete_ticket(ticket_id)
        return self.send_json(result)
