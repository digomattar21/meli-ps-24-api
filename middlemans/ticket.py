from heart.structures.verify import verifyJson
from heart.validators.ticket import ticketTypes
from utils.apiMessages import errorMessage, LocalApiCode
from utils.checkTypes import checkFieldType

def verifyTicketGet(next):
    def decorator(self, **data):
        id = self.getParameter("id", None)
        
        data.update({
            "id": id,
        })
        return next(self, **data)
    return decorator

def verifyTicketCreate(next):
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