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


def verify_ticket_exists(next):
    def decorator(self, ticket_id=None, **data):
        ticket = TicketGateway.get_by_id(ticket_id)
        if not ticket:
            return {"errors": [error_message(LocalApiCode.ticketNotFound)]}
        return next(self, ticket_id=ticket_id, **data)

    return decorator


def verify_ticket_patch(next):
    def decorator(self, ticket_id=None, **data):
        body = self.get_json_body()
        if not body:
            return self.send_json(
                {"errors": [error_message(LocalApiCode.emptyRequest)]}
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

        if "title" in body and (body["title"] is None or body["title"].strip() == ""):
            return self.send_json(
                {"errors": [error_message(LocalApiCode.invalidTitle)]}
            )

        if "description" in body and (
            body["description"] is None or body["description"].strip() == ""
        ):
            return self.send_json(
                {"errors": [error_message(LocalApiCode.invalidDescription)]}
            )

        if errors:
            return self.send_json({"errors": errors})

        data.update(body)

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

        if body["title"] == "" or not body["title"]:
            return self.send_json(
                {"errors": [error_message(LocalApiCode.invalidTitle)]}
            )

        if body["description"] == "" or not body["description"]:
            return self.send_json(
                {"errors": [error_message(LocalApiCode.invalidDescription)]}
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
