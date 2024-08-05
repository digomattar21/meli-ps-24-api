from gateways.severity import SeverityGateway
from gateways.ticket import TicketGateway
from heart.validators.severity import SEVERITY_DESCRIPTIONS
from utils.apiMessages import LocalApiCode, error_message


class SeverityService:

    @classmethod
    def get_severity_by_id(cls, severity_id):
        severity = SeverityGateway.get_by_id(severity_id)
        if not severity:
            return {"errors": [error_message(LocalApiCode.severityNotFound)]}
        return {"severity": severity.to_dict()}

    @classmethod
    def get_all_severities(cls):
        severities = SeverityGateway.get_all()
        return [severity.to_dict() for severity in severities]

    @classmethod
    def create_severity(cls, level):
        if level not in SEVERITY_DESCRIPTIONS.keys():
            return {"errors": [error_message(LocalApiCode.invalidSeverityLevel)]}

        if SeverityGateway.get_by_level(level):
            return {"errors": [error_message(LocalApiCode.duplicateSeverityLevel)]}

        description = SEVERITY_DESCRIPTIONS[level]
        severity = SeverityGateway.create(level=level, description=description)
        if severity:
            return {"severity_id": severity.id}

        return {"errors": [error_message(LocalApiCode.internalError)]}

    @classmethod
    def update_severity(cls, severity_id, **data):
        level = data.get("level")
        if level == 1:
            tickets_with_severity = TicketGateway.get_by_severity_id(severity_id)
            if tickets_with_severity:
                return {"errors": [error_message(LocalApiCode.severityLevelOneInUse)]}

        if SeverityGateway.get_by_level(level):
            return {"errors": [error_message(LocalApiCode.duplicateSeverityLevel)]}

        data["description"] = SEVERITY_DESCRIPTIONS[level]
        try:
            updated_severity = SeverityGateway.update(severity_id, **data)
            print(updated_severity)
        except Exception as e:
            print(e)

        if not updated_severity:
            return {"errors": [error_message(LocalApiCode.internalError)]}

        return {"severity": updated_severity.to_dict()}

    @classmethod
    def delete_severity(cls, severity_id):
        tickets_with_severity = TicketGateway.get_by_severity_id(severity_id)
        if tickets_with_severity:
            return {"errors": [error_message(LocalApiCode.severityInUse)]}

        try:
            SeverityGateway.delete(severity_id)
        except Exception as e:
            print(e)
            return {"errors": [error_message(LocalApiCode.internalError)]}

        return {"message": "Severity deleted successfully"}
