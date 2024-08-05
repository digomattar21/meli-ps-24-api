import random

from gateways.category import CategoryGateway
from gateways.severity import SeverityGateway
from gateways.ticket import TicketGateway
from gateways.user import UserGateway
from utils.apiMessages import LocalApiCode, error_message


class TicketService:

    @classmethod
    def get_all_tickets(cls):
        tickets = TicketGateway.get_all()
        if not tickets:
            return {"errors": [error_message(LocalApiCode.ticketNotFound)]}
        return {"tickets": [ticket.to_dict() for ticket in tickets]}

    @classmethod
    def get_ticket_by_id(cls, ticket_id):
        ticket = TicketGateway.get_by_id(ticket_id)
        if not ticket:
            return {"errors": [error_message(LocalApiCode.ticketNotFound)]}
        return {"ticket": ticket.to_dict()}

    @classmethod
    def create_ticket(
        cls, title, description, category_id, subcategory_id, severity_id
    ):
        category = CategoryGateway.get_by_id(category_id)
        if not category:
            return {"errors": [error_message(LocalApiCode.categoryNotFound)]}

        subcategory = CategoryGateway.get_by_id(subcategory_id)
        if not subcategory:
            return {"errors": [error_message(LocalApiCode.invalidSubcategory)]}
        if subcategory.parent_id != category.id:
            return {"errors": [error_message(LocalApiCode.isNotSubcategory)]}

        severity = SeverityGateway.get_by_id(severity_id)
        if not severity:
            return {"errors": [error_message(LocalApiCode.severityNotFound)]}
        if severity.level == 1:
            return {"errors": [error_message(LocalApiCode.invalidSeverity)]}

        users = UserGateway.get_all_users()
        selected_user = cls._select_user_with_least_tickets(users)

        ticket = TicketGateway.create(
            title=title,
            description=description,
            category_id=category_id,
            subcategory_id=subcategory_id,
            severity_id=severity_id,
            user_id=selected_user["id"] if selected_user else None,
        )

        return {"ticket": ticket.to_dict()}

    @classmethod
    def update_ticket(cls, ticket_id, **data):
        ticket = TicketGateway.get_by_id(ticket_id)
        if not ticket:
            return {"errors": [error_message(LocalApiCode.ticketNotFound)]}
        if "category_id" in data:
            category = CategoryGateway.get_by_id(data["category_id"])
            if not category:
                return {"errors": [error_message(LocalApiCode.categoryNotFound)]}
            data["category_id"] = data["category_id"]

            if "subcategory_id" in data or ticket.subcategory_id:
                subcategory_id = data.get("subcategory_id", ticket.subcategory_id)
                subcategory = CategoryGateway.get_by_id(subcategory_id)
                if not subcategory or subcategory.parent_id != category.id:
                    return {"errors": [error_message(LocalApiCode.isNotSubcategory)]}
                data["subcategory_id"] = subcategory_id

        if "severity_id" in data:
            severity = SeverityGateway.get_by_id(data["severity_id"])
            if not severity or severity.level == 1:
                return {"errors": [error_message(LocalApiCode.invalidSeverity)]}
            data["severity_id"] = severity.id

        updated_ticket = TicketGateway.update(ticket_id, **data)
        if not updated_ticket:
            return {"errors": [error_message(LocalApiCode.internalError)]}

        return {"ticket": updated_ticket.to_dict()}

    @classmethod
    def delete_ticket(cls, ticket_id):
        ticket = TicketGateway.get_by_id(ticket_id)
        if not ticket:
            return {"errors": [error_message(LocalApiCode.ticketNotFound)]}

        TicketGateway.delete(ticket_id)
        return {"message": "Ticket deleted successfully"}

    @staticmethod
    def _select_user_with_least_tickets(users):
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

        return selected_user
