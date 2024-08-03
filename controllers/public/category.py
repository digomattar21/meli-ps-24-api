from heart.server.controller import BaseController
from gateways.category import CategoryGateway
from utils.apiMessages import errorMessage, LocalApiCode
from middlemans.category import verifyCategoryGet, verifyCategoryPost, verifyCategoryPatch, verifyCategoryDelete

class CategoryController(BaseController):

    @verifyCategoryGet
    def get(self, category_id=None):
        if category_id:
            category = CategoryGateway.get_by_id(category_id)
            if category:
                return self.sendJson({"category": category.to_dict(include_subcategories=True)})
            return self.sendJson({"errors": [errorMessage(LocalApiCode.categoryNotFound)]})
        
        categories = CategoryGateway.get_all()
        return self.sendJson({"categories": [category.to_dict(include_subcategories=True) for category in categories]})

    @verifyCategoryPost
    def post(self, **data):
        name = data.get('name')
        parent_id = data.get('parent_id')

        category = CategoryGateway.create(name=name, parent_id=parent_id)
        if category:
            return self.sendJson({"category_id": category.id})
        else:
            return self.sendJson({"errors": [errorMessage(LocalApiCode.duplicateCategoryName)]})

    @verifyCategoryPatch
    def patch(self, category_id, **data):
        category = CategoryGateway.update(category_id, **data)
        if category:
            return self.sendJson({"category": category.to_dict()})
        return self.sendJson({"errors": [errorMessage(LocalApiCode.categoryNotFound)]})

    @verifyCategoryDelete
    def delete(self, category_id):
        CategoryGateway.delete(category_id)
        return self.sendJson({"message": "Category deleted successfully"})
