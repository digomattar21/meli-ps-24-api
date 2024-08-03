from heart.structures.verify import verifyJson
from heart.validators.category import categoryTypes
from utils.apiMessages import errorMessage, LocalApiCode
from utils.checkTypes import checkFieldType
from gateways.category import CategoryGateway

def verifyCategoryGet(next):
    def decorator(self, category_id=None, **data):
        if category_id is not None:
            data["category_id"] = category_id
        return next(self, **data)
    return decorator

def verifyCategoryDelete(next):
    def decorator(self, category_id):
        category = CategoryGateway.get_by_id(category_id)
        if not category:
            return self.sendJson({"errors": [errorMessage(LocalApiCode.categoryNotFound)]})
        
        return next(self, category_id=category_id)
    return decorator

def verifyCategoryPatch(next):
    def decorator(self, category_id, **data):
        body = self.getJsonBody()
        if not body:
            return self.sendJson({"errors": [errorMessage(LocalApiCode.emptyRequest)]})

        category = CategoryGateway.get_by_id(category_id)
        if not category:
            return self.sendJson({"errors": [errorMessage(LocalApiCode.categoryNotFound)]})
        
        errors = verifyJson(
            json=body,
            requiredParameters=[],
            optionalParameters=["name", "parent_id"]
        )
        
        if errors:
            return self.sendJson({"errors": errors})
        
        if "name" in body:
            if body["name"] is None:
                return self.sendJson({"errors": [errorMessage(LocalApiCode.invalidCategoryName)]})
            already_exists = CategoryGateway.get_by_name(body["name"])
            if already_exists:
                return self.sendJson({"errors": [errorMessage(LocalApiCode.duplicateCategoryName)]})
            
            data["name"] = body["name"]

        if "parent_id" in body:
            if body["parent_id"] in [None, False]:
                data["parent_id"] = None
            else:
                parent_category = CategoryGateway.get_by_id(body["parent_id"])
                if not parent_category:
                    return self.sendJson({"errors": [errorMessage(LocalApiCode.invalidParentCategory)]})
                data["parent_id"] = body["parent_id"]
        
        return next(self, category_id=category_id, **data)
    return decorator
        
        
def verifyCategoryPost(next):
    def decorator(self , **data):
        body = self.getJsonBody()
        if not body:
            return self.sendJson({"errors": [errorMessage(LocalApiCode.emptyRequest)]})
        
        errors = verifyJson(
            json=body,
            requiredParameters=[
                "name",
            ],
            optionalParameters=["parent_id"],
        )
       
        if errors:
            return self.sendJson({"errors": errors})
        
        errors = validateCategoryFields(body)
        
        if errors:
            return self.sendJson({"errors": errors})
        
        if "parent_id" in body:
            parent_category =CategoryGateway.get_by_id(body["parent_id"])
            if not parent_category:
                return self.sendJson({"errors":[errorMessage(LocalApiCode.invalidParentCategory)]})

        data.update({
            "name": body["name"],
            "parent_id": body.get("parent_id", None),
        })
        
        return next(self, **data)
    return decorator


def validateCategoryFields(data):
    errors = []
    for parameter, expectedType in categoryTypes.items():
        value = data.get(parameter)
        if value is not None:
            valid, message = checkFieldType(parameter, value, expectedType)
            if not valid:
                errors.append(message)
    
    return errors