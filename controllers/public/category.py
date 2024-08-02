from heart.server.controller import BaseController
from gateways.category import CategoryGateway

class CategoryController(BaseController):

    def get(self, **data):
        category_id = data.get('id')
        if category_id:
            category = CategoryGateway.get_by_id(category_id)
            if category:
                return self.sendJson({"category": category.to_dict()})
            return self.sendError("Category not found", 404)
        
        categories = CategoryGateway.get_all()
        return self.sendJson({"categories": [category.to_dict() for category in categories]})

    def post(self, **data):
        name = data.get('name')
        parent_id = data.get('parent_id')

        category = CategoryGateway.create(name=name, parent_id=parent_id)
        return self.sendJson({"category_id": category.id}, 201)

    def patch(self, **data):
        category_id = data.get('id')
        category = CategoryGateway.update(category_id, **data)
        if category:
            return self.sendJson({"category": category.to_dict()})
        return self.sendError("Failed to update category", 400)

    def delete(self, **data):
        category_id = data.get('id')
        CategoryGateway.delete(category_id)
        return self.sendJson({"message": "Category deleted successfully"})
