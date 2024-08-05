from heart.server.controller import BaseController
from middlemans.category import (
    verify_category_exists,
    verify_category_get,
    verify_category_patch,
    verify_category_post,
)
from services.category import CategoryService


class CategoryController(BaseController):

    @verify_category_get
    def get(self, category_id=None):
        if category_id:
            result = CategoryService.get_category_by_id(category_id)
            if "errors" in result:
                return self.send_json(result)
            return self.send_json({"category": result})

        categories = CategoryService.get_all_categories()
        return self.send_json({"categories": categories})

    @verify_category_post
    def post(self, **data):
        result = CategoryService.create_category(
            data.get("name"), data.get("parent_id")
        )
        if "errors" in result:
            return self.send_json(result)
        return self.send_json(result)

    @verify_category_exists
    @verify_category_patch
    def patch(self, category_id, **data):
        result = CategoryService.update_category(category_id, **data)
        return self.send_json(result)

    @verify_category_exists
    def delete(self, category_id):
        result = CategoryService.delete_category(category_id)
        return self.send_json(result)
