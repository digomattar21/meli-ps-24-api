import random

from gateways.ticket import TicketGateway
from gateways.user import UserGateway
from heart.server.controller import BaseController
from middlemans.ticket import (
    verify_ticket_delete,
    verify_ticket_get,
    verify_ticket_patch,
    verify_ticket_post,
)
from utils.apiMessages import LocalApiCode, error_message


class TicketController(BaseController):

    @verify_ticket_get
    def get(self, ticket_id=None, **data):
        if ticket_id:
            ticket = TicketGateway.get_by_id(ticket_id)
            if ticket:
                return self.send_json({"ticket": ticket.to_dict()})
            return self.send_json(
                {"errors": [error_message(LocalApiCode.ticketNotFound)]}
            )

        tickets = TicketGateway.get_all()
        return self.send_json({"tickets": [ticket.to_dict() for ticket in tickets]})

    @verify_ticket_post
    def post(self, **data):
        title = data.get("title")
        description = data.get("description")
        category_id = data.get("category_id")
        subcategory_id = data.get("subcategory_id")
        severity_id = data.get("severity_id")

        users = UserGateway.get_all_users()

        min_tickets = float("inf")
        selected_user = None

        for user in users:
            tickets = TicketGateway.get_by_user_id(user["id"])
            ticket_count = len(tickets)

            if ticket_count < min_tickets or (
                ticket_count == min_tickets and random.choice([True, False])
            ):
                min_tickets = ticket_count
                selected_user = user

        new_ticket = TicketGateway.create(
            title=title,
            description=description,
            category_id=category_id,
            subcategory_id=subcategory_id,
            severity_id=severity_id,
            user_id=selected_user["id"] if selected_user else None,
        )

        return self.send_json({"ticket": new_ticket.to_dict()})

    @verify_ticket_patch
    def patch(self, ticket_id, **data):
        updated_ticket = TicketGateway.update(ticket_id, **data)
        if updated_ticket:
            return self.send_json({"ticket": updated_ticket.to_dict()})

        return self.send_json({"errors": [error_message(LocalApiCode.internalError)]})

    @verify_ticket_delete
    def delete(self, ticket_id):
        TicketGateway.delete(ticket_id)
        return self.send_json({"message": "Ticket deleted successfully"})
