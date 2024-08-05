from gateways.severity import SeverityGateway
from gateways.ticket import TicketGateway
from heart.structures.verify import verify_json
from heart.validators.severity import SEVERITY_TYPES
from utils.apiMessages import LocalApiCode, error_message
from utils.checkTypes import check_field_type


def verify_severity_get(next):
    def decorator(self, severity_id=None, **data):
        if severity_id is not None:
            data["severity_id"] = severity_id
        return next(self, **data)

    return decorator


def verify_severity_delete(next):
    def decorator(self, severity_id):
        severity = SeverityGateway.get_by_id(severity_id)
        if not severity:
            return self.send_json(
                {"errors": [error_message(LocalApiCode.severityNotFound)]}
            )

        tickets_with_severity = TicketGateway.get_by_severity_id(severity_id)
        if tickets_with_severity:
            return self.send_json(
                {"errors": [error_message(LocalApiCode.severityInUse)]}
            )

        return next(self, severity_id=severity_id)

    return decorator


def verify_severity_patch(next):
    def decorator(self, severity_id, **data):
        body = self.get_json_body()
        if not body:
            return self.send_json(
                {"errors": [error_message(LocalApiCode.emptyRequest)]}
            )

        severity = SeverityGateway.get_by_id(severity_id)
        if not severity:
            return self.send_json(
                {"errors": [error_message(LocalApiCode.severityNotFound)]}
            )

        errors = verify_json(
            json=body, requiredParameters=["level"], optionalParameters=[]
        )

        if errors:
            return self.send_json({"errors": errors})

        level = body.get("level")
        if not isinstance(level, int) or level not in [1, 2, 3, 4]:
            return self.send_json(
                {"errors": [error_message(LocalApiCode.invalidSeverityLevel)]}
            )

        if level == 1:
            tickets_with_severity = TicketGateway.get_by_severity_id(severity_id)
            if tickets_with_severity:
                return self.send_json(
                    {"errors": [error_message(LocalApiCode.severityLevelOneInUse)]}
                )

        severity = SeverityGateway.get_by_level(level=level)
        if severity:
            return self.send_json(
                {"errors": error_message(LocalApiCode.duplicateSeverityLevel)}
            )

        data.update(
            {
                "level": level,
            }
        )

        return next(self, severity_id=severity_id, **data)

    return decorator


def verify_severity_post(next):
    def decorator(self, **data):
        body = self.get_json_body()
        if not body:
            return self.send_json(
                {"errors": [error_message(LocalApiCode.emptyRequest)]}
            )

        errors = verify_json(
            json=body,
            requiredParameters=[
                "level",
            ],
            optionalParameters=[],
        )

        if errors:
            return self.send_json({"errors": errors})

        errors = validate_severity_fields(body)

        if errors:
            return self.send_json({"errors": errors})

        level = body.get("level")
        if not isinstance(level, int) or level not in [1, 2, 3, 4]:
            return self.send_json(
                {"errors": [error_message(LocalApiCode.invalidSeverityLevel)]}
            )

        severity = SeverityGateway.get_by_level(level=level)
        if severity:
            return self.send_json(
                {"errors": error_message(LocalApiCode.duplicateSeverityLevel)}
            )

        data.update(
            {
                "level": body["level"],
            }
        )

        return next(self, **data)

    return decorator


def validate_severity_fields(data):
    errors = []
    for parameter, expectedType in SEVERITY_TYPES.items():
        value = data.get(parameter)
        if value is not None:
            valid, message = check_field_type(parameter, value, expectedType)
            if not valid:
                errors.append(message)

    return errors
