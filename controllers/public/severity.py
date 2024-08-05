from heart.server.controller import BaseController
from middlemans.severity import (
    verify_severity_exists,
    verify_severity_get,
    verify_severity_patch,
    verify_severity_post,
)
from services.severity import SeverityService


class SeverityController(BaseController):

    @verify_severity_get
    def get(self, severity_id=None):
        if severity_id:
            return self.send_json(SeverityService.get_severity_by_id(severity_id))

        return self.send_json({"severities": SeverityService.get_all_severities()})

    @verify_severity_post
    def post(self, **data):
        return self.send_json(SeverityService.create_severity(data.get("level")))

    @verify_severity_exists
    @verify_severity_patch
    def patch(self, severity_id, **data):
        return self.send_json(SeverityService.update_severity(severity_id, **data))

    @verify_severity_exists
    def delete(self, severity_id):
        return self.send_json(SeverityService.delete_severity(severity_id))
