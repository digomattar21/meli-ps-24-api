from heart.structures.verify import verify_json
from heart.validators.category import CATEGORY_TYPES
from utils.apiMessages import error_message, LocalApiCode
from utils.checkTypes import check_field_type
from gateways.category import CategoryGateway

def verify_category_get(next):
    def decorator(self, category_id=None, **data):
        if category_id is not None:
            data["category_id"] = category_id
        return next(self, **data)
    return decorator

def verify_category_delete(next):
    def decorator(self, category_id):
        category = CategoryGateway.get_by_id(category_id)
        if not category:
            return self.send_json({"errors": [error_message(LocalApiCode.categoryNotFound)]})
        
        return next(self, category_id=category_id)
    return decorator

def verify_category_patch(next):
    def decorator(self, category_id, **data):
        body = self.get_json_body()
        if not body:
            return self.send_json({"errors": [error_message(LocalApiCode.emptyRequest)]})

        category = CategoryGateway.get_by_id(category_id)
        if not category:
            return self.send_json({"errors": [error_message(LocalApiCode.categoryNotFound)]})
        
        errors = verify_json(
            json=body,
            requiredParameters=[],
            optionalParameters=["name", "parent_id"]
        )
        
        if errors:
            return self.send_json({"errors": errors})
        
        if "name" in body:
            if body["name"] is None:
                return self.send_json({"errors": [error_message(LocalApiCode.invalidCategoryName)]})
            already_exists = CategoryGateway.get_by_name(body["name"])
            if already_exists:
                return self.send_json({"errors": [error_message(LocalApiCode.duplicateCategoryName)]})
            
            data["name"] = body["name"]

        if "parent_id" in body:
            if body["parent_id"] in [None, False]:
                data["parent_id"] = None
            else:
                parent_category = CategoryGateway.get_by_id(body["parent_id"])
                if not parent_category:
                    return self.send_json({"errors": [error_message(LocalApiCode.invalidParentCategory)]})
                data["parent_id"] = body["parent_id"]
        
        return next(self, category_id=category_id, **data)
    return decorator
        
        
def verify_category_post(next):
    def decorator(self , **data):
        body = self.get_json_body()
        if not body:
            return self.send_json({"errors": [error_message(LocalApiCode.emptyRequest)]})
        
        errors = verify_json(
            json=body,
            requiredParameters=[
                "name",
            ],
            optionalParameters=["parent_id"],
        )
       
        if errors:
            return self.send_json({"errors": errors})
        
        errors = validate_category_fields(body)
        
        if errors:
            return self.send_json({"errors": errors})
        
        if "parent_id" in body:
            parent_category =CategoryGateway.get_by_id(body["parent_id"])
            if not parent_category:
                return self.send_json({"errors":[error_message(LocalApiCode.invalidParentCategory)]})

        data.update({
            "name": body["name"],
            "parent_id": body.get("parent_id", None),
        })
        
        return next(self, **data)
    return decorator


def validate_category_fields(data):
    errors = []
    for parameter, expectedType in CATEGORY_TYPES.items():
        value = data.get(parameter)
        if value is not None:
            valid, message = check_field_type(parameter, value, expectedType)
            if not valid:
                errors.append(message)
    
    return errors