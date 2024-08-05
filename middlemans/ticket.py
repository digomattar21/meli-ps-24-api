from gateways.category import CategoryGateway
from gateways.severity import SeverityGateway
from gateways.ticket import TicketGateway
from heart.structures.verify import verify_json
from heart.validators.ticket import TICKET_TYPES
from utils.apiMessages import LocalApiCode, error_message
from utils.checkTypes import check_field_type


def verify_ticket_get(next):
    def decorator(self, ticket_id=None, **data):
        if ticket_id is not None:
            data["ticket_id"] = ticket_id
        return next(self, **data)

    return decorator


def verify_ticket_delete(next):
    def decorator(self, ticket_id, **data):
        ticket = TicketGateway.get_by_id(ticket_id)
        if not ticket:
            return self.send_json(
                {"errors": [error_message(LocalApiCode.ticketNotFound)]}
            )

        return next(self, ticket_id=ticket_id, **data)

    return decorator


def verify_ticket_patch(next):
    def decorator(self, ticket_id, **data):
        body = self.get_json_body()
        if not body:
            return self.send_json(
                {"errors": [error_message(LocalApiCode.emptyRequest)]}
            )

        ticket = TicketGateway.get_by_id(ticket_id)
        if not ticket:
            return self.send_json(
                {"errors": [error_message(LocalApiCode.ticketNotFound)]}
            )

        errors = verify_json(
            json=body,
            requiredParameters=[],
            optionalParameters=[
                "title",
                "description",
                "category_id",
                "subcategory_id",
                "severity_id",
            ],
        )

        if errors:
            return self.send_json({"errors": errors})

        errors = validate_ticket_fields(body)
        if errors:
            return self.send_json({"errors": errors})

        if "category_id" in body:
            category = CategoryGateway.get_by_id(body["category_id"])
            if not category:
                return self.send_json(
                    {"errors": [error_message(LocalApiCode.categoryNotFound)]}
                )
            data["category_id"] = body["category_id"]

            if "subcategory_id" not in body and ticket.subcategory_id:
                subcategory = CategoryGateway.get_by_id(ticket.subcategory_id)
                if subcategory.parent_id != body["category_id"]:
                    return self.send_json(
                        {"errors": [error_message(LocalApiCode.isNotSubcategory)]}
                    )

        if "subcategory_id" in body:
            subcategory = CategoryGateway.get_by_id(body["subcategory_id"])
            if not subcategory:
                return self.send_json(
                    {"errors": [error_message(LocalApiCode.invalidSubcategory)]}
                )
            if subcategory.parent_id != body.get("category_id", ticket.category_id):
                return self.send_json(
                    {"errors": [error_message(LocalApiCode.isNotSubcategory)]}
                )
            data["subcategory_id"] = body["subcategory_id"]

        if "severity_id" in body:
            severity = SeverityGateway.get_by_level(body["severity_id"])
            if not severity:
                return self.send_json(
                    {"errors": [error_message(LocalApiCode.severityNotFound)]}
                )
            if severity.level == 1:
                return self.send_json(
                    {"errors": [error_message(LocalApiCode.invalidSeverity)]}
                )
            data["severity_id"] = severity.id

        if "title" in body:
            if body["title"] is None:
                return self.send_json(
                    {"errors": [error_message(LocalApiCode.invalidTitle)]}
                )
            data["title"] = body["title"]

        if "description" in body:
            if body["description"] is None:
                return self.send_json(
                    {"errors": [error_message(LocalApiCode.invalidDescription)]}
                )
            data["description"] = body["description"]

        return next(self, ticket_id=ticket_id, **data)

    return decorator


def verify_ticket_post(next):
    def decorator(self, **data):
        body = self.get_json_body()
        if not body:
            return self.send_json(
                {"errors": [error_message(LocalApiCode.emptyRequest)]}
            )

        errors = verify_json(
            json=body,
            requiredParameters=[
                "title",
                "description",
                "severity_id",
                "category_id",
                "subcategory_id",
            ],
            optionalParameters=[],
        )

        if errors:
            return self.send_json({"errors": errors})

        errors = validate_ticket_fields(body)

        if errors:
            return self.send_json({"errors": errors})

        severity = SeverityGateway.get_by_id(body["severity_id"])

        if not severity:
            return self.send_json(
                {"errors": error_message(LocalApiCode.severityNotFound)}
            )

        if severity.level == 1:
            return self.send_json(
                {"errors": [error_message(LocalApiCode.invalidSeverity)]}
            )

        category = CategoryGateway.get_by_id(body["category_id"])
        if not category:
            return self.send_json(
                {"errors": [error_message(LocalApiCode.categoryNotFound)]}
            )

        subcategory = CategoryGateway.get_by_id(body["subcategory_id"])
        if not subcategory:
            return self.send_json(
                {"errors": [error_message(LocalApiCode.invalidSubcategory)]}
            )

        if subcategory.parent_id is None or subcategory.parent_id != category.id:
            return self.send_json(
                {"errors": [error_message(LocalApiCode.isNotSubcategory)]}
            )

        data.update(
            {
                "title": body["title"],
                "description": body["description"],
                "severity_id": body["severity_id"],
                "category_id": body["category_id"],
                "subcategory_id": body["subcategory_id"],
            }
        )

        return next(self, **data)

    return decorator


def validate_ticket_fields(data):
    errors = []
    for parameter, expectedType in TICKET_TYPES.items():
        value = data.get(parameter)
        if value is not None:
            valid, message = check_field_type(parameter, value, expectedType)
            if not valid:
                errors.append(message)

    return errors
