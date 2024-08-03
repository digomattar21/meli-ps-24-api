from heart.structures.verify import verifyJson
from heart.validators.ticket import ticketTypes
from utils.apiMessages import errorMessage, LocalApiCode
from utils.checkTypes import checkFieldType
from gateways.category import CategoryGateway
from gateways.severity import SeverityGateway
from gateways.ticket import TicketGateway

def verifyTicketGet(next):
    def decorator(self, ticket_id=None, **data):
        if ticket_id is not None:
            data["ticket_id"] = ticket_id
        return next(self, **data)
    return decorator

def verifyTicketDelete(next):
    def decorator(self, ticket_id, **data):
        ticket = TicketGateway.get_by_id(ticket_id)
        if not ticket:
            return self.sendJson({"errors": [errorMessage(LocalApiCode.ticketNotFound)]})
        
        return next(self, ticket_id=ticket_id, **data)
    return decorator

def verifyTicketPatch(next):
    def decorator(self, ticket_id, **data):
        body = self.getJsonBody()
        if not body:
            return self.sendJson({"errors": [errorMessage(LocalApiCode.emptyRequest)]})
        
        ticket = TicketGateway.get_by_id(ticket_id)
        if not ticket:
            return self.sendJson({"errors": [errorMessage(LocalApiCode.ticketNotFound)]})

        errors = verifyJson(
            json=body,
            requiredParameters=[],
            optionalParameters=["title", "description", "category_id", "subcategory_id", "severity"]
        )
        
        if errors:
            return self.sendJson({"errors": errors})
        
        errors = validateTicketFields(body)
        if errors:
            return self.sendJson({"errors": errors})

        if "category_id" in body:
            category = CategoryGateway.get_by_id(body["category_id"])
            if not category:
                return self.sendJson({"errors": [errorMessage(LocalApiCode.categoryNotFound)]})
            data["category_id"] = body["category_id"]

            if "subcategory_id" not in body and ticket.subcategory_id:
                subcategory = CategoryGateway.get_by_id(ticket.subcategory_id)
                if subcategory.parent_id != body["category_id"]:
                    return self.sendJson({"errors": [errorMessage(LocalApiCode.isNotSubcategory)]})

        if "subcategory_id" in body:
            subcategory = CategoryGateway.get_by_id(body["subcategory_id"])
            if not subcategory:
                return self.sendJson({"errors": [errorMessage(LocalApiCode.invalidSubcategory)]})
            if subcategory.parent_id != body.get("category_id", ticket.category_id):
                return self.sendJson({"errors": [errorMessage(LocalApiCode.isNotSubcategory)]})
            data["subcategory_id"] = body["subcategory_id"]

        if "severity" in body:
            severity = SeverityGateway.get_by_level(body["severity"])
            if not severity:
                return self.sendJson({"errors": [errorMessage(LocalApiCode.invalidSeverity)]})
            if severity.level == 1: 
                return self.sendJson({"errors": [errorMessage(LocalApiCode.invalidSeverity)]})
            data["severity_id"] = severity.id

        if "title" in body:
            if body["title"] is None:
                return self.sendJson({"errors": [errorMessage(LocalApiCode.invalidTitle)]})
            data["title"] = body["title"]

        if "description" in body:
            if body["description"] is None:
                return self.sendJson({"errors": [errorMessage(LocalApiCode.invalidDescription)]})
            data["description"] = body["description"]
        
        return next(self, ticket_id=ticket_id, **data)
    return decorator

def verifyTicketPost(next):
    def decorator(self , **data):
        body = self.getJsonBody()
        if not body:
            return self.sendJson({"errors": [errorMessage(LocalApiCode.emptyRequest)]})
        
        errors = verifyJson(
            json=body,
            requiredParameters=[
                "title", "description", "severity", "category", "subcategory"
            ],
            optionalParameters=[],
        )
       
        if errors:
            return self.sendJson({"errors": errors})
        
        errors = validateTicketFields(body)
        
        if errors:
            return self.sendJson({"errors": errors})
        
        if body["severity"] == 1:
            return self.sendJson({"errors": [errorMessage(LocalApiCode.invalidSeverity)]})
        
        category = CategoryGateway.get_by_id(body["category"])
        if not category:
            return self.sendJson({"errors": [errorMessage(LocalApiCode.categoryNotFound)]})

        subcategory = CategoryGateway.get_by_id(body["subcategory"])
        if not subcategory:
            return self.sendJson({"errors": [errorMessage(LocalApiCode.invalidSubcategory)]})
        
        if subcategory.parent_id is None or subcategory.parent_id != category.id:
            return self.sendJson({"errors": [errorMessage(LocalApiCode.isNotSubcategory)]})
    
        data.update({
            "title": body["title"],
            "description": body["description"],
            "severity": body["severity"],
            "category_id": body["category"],
            "subcategory_id": body["subcategory"],
        })
        
        return next(self, **data)
    return decorator

def validateTicketFields(data):
    errors = []
    for parameter, expectedType in ticketTypes.items():
        value = data.get(parameter)
        if value is not None:
            valid, message = checkFieldType(parameter, value, expectedType)
            if not valid:
                errors.append(message)
    
    return errors