from gateways.severity import SeverityGateway
from heart.server.controller import BaseController
from middlemans.severity import (
    verify_severity_delete,
    verify_severity_get,
    verify_severity_patch,
    verify_severity_post,
)
from utils.apiMessages import LocalApiCode, error_message


class SeverityController(BaseController):

    SEVERITY_DESCRIPTIONS = {
        1: "Issue High",
        2: "High",
        3: "Medium",
        4: "Low",
    }

    @verify_severity_get
    def get(self, severity_id=None):
        if severity_id:
            severity = SeverityGateway.get_by_id(severity_id)
            if severity:
                return self.send_json({"severity": severity.to_dict()})
            return self.send_json(
                {"errors": [error_message(LocalApiCode.severityNotFound)]}
            )

        severities = SeverityGateway.get_all()
        return self.send_json(
            {"severities": [severity.to_dict() for severity in severities]}
        )

    @verify_severity_post
    def post(self, **data):
        level = data.get("level")

        if level not in self.SEVERITY_DESCRIPTIONS.keys():
            return self.send_json(
                {"errors": [error_message(LocalApiCode.invalidSeverityLevel)]}
            )

        description = self.SEVERITY_DESCRIPTIONS[level]
        severity = SeverityGateway.create(level=level, description=description)
        if severity:
            return self.send_json({"severity_id": severity.id})
        else:
            return self.send_json(
                {"errors": [error_message(LocalApiCode.duplicateSeverityLevel)]}
            )

    @verify_severity_patch
    def patch(self, severity_id, **data):
        level = data.get("level")

        if level and level not in self.SEVERITY_DESCRIPTIONS.keys():
            return self.send_json(
                {"errors": [error_message(LocalApiCode.invalidSeverityLevel)]}
            )

        if level:
            data["description"] = self.SEVERITY_DESCRIPTIONS[level]

        severity = SeverityGateway.update(severity_id, **data)
        if severity:
            return self.send_json({"severity": severity.to_dict()})
        return self.send_json(
            {"errors": [error_message(LocalApiCode.severityNotFound)]}
        )

    @verify_severity_delete
    def delete(self, severity_id):
        SeverityGateway.delete(severity_id)
        return self.send_json({"message": "Severity deleted successfully"})
