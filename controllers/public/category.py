from gateways.category import CategoryGateway
from heart.server.controller import BaseController
from middlemans.category import (
    verify_category_delete,
    verify_category_get,
    verify_category_patch,
    verify_category_post,
)
from utils.apiMessages import LocalApiCode, error_message


class CategoryController(BaseController):

    @verify_category_get
    def get(self, category_id=None):
        if category_id:
            category = CategoryGateway.get_by_id(category_id)
            if category:
                return self.send_json(
                    {"category": category.to_dict(include_subcategories=True)}
                )
            return self.send_json(
                {"errors": [error_message(LocalApiCode.categoryNotFound)]}
            )

        categories = CategoryGateway.get_all()
        return self.send_json(
            {
                "categories": [
                    category.to_dict(include_subcategories=True)
                    for category in categories
                ]
            }
        )

    @verify_category_post
    def post(self, **data):
        name = data.get("name")
        parent_id = data.get("parent_id")

        category = CategoryGateway.create(name=name, parent_id=parent_id)
        if category:
            return self.send_json({"category_id": category.id})
        else:
            return self.send_json(
                {"errors": [error_message(LocalApiCode.duplicateCategoryName)]}
            )

    @verify_category_patch
    def patch(self, category_id, **data):
        category = CategoryGateway.update(category_id, **data)
        if category:
            return self.send_json({"category": category.to_dict()})
        return self.send_json(
            {"errors": [error_message(LocalApiCode.categoryNotFound)]}
        )

    @verify_category_delete
    def delete(self, category_id):
        CategoryGateway.delete(category_id)
        return self.send_json({"message": "Category deleted successfully"})
