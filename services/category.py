from sqlalchemy.exc import IntegrityError

from gateways.category import CategoryGateway
from gateways.ticket import TicketGateway
from utils.apiMessages import LocalApiCode, error_message


class CategoryService:

    @classmethod
    def create_category(cls, name, parent_id=None):
        try:
            if parent_id:
                parent_category = CategoryGateway.get_by_id(parent_id)
                if not parent_category:
                    return {
                        "errors": [error_message(LocalApiCode.invalidParentCategory)]
                    }
            category = CategoryGateway.create(name=name, parent_id=parent_id)
            if not category:
                return {"errors": [error_message(LocalApiCode.duplicateCategoryName)]}
            return {"category_id": category.id}
        except IntegrityError:
            return {"errors": [error_message(LocalApiCode.internalServerError)]}

    @classmethod
    def get_category_by_id(cls, category_id):
        category = CategoryGateway.get_by_id(category_id)
        if not category:
            return {"errors": [error_message(LocalApiCode.categoryNotFound)]}
        return category.to_dict(include_subcategories=True)

    @classmethod
    def get_all_categories(cls):
        categories = CategoryGateway.get_all()
        return [category.to_dict(include_subcategories=True) for category in categories]

    @classmethod
    def update_category(cls, category_id, **data):
        if "name" in data:
            if data["name"] is None:
                return {"errors": [error_message(LocalApiCode.invalidCategoryName)]}
            already_exists = CategoryGateway.get_by_name(data["name"])
            if already_exists:
                return {"errors": [error_message(LocalApiCode.duplicateCategoryName)]}

        if "parent_id" in data:
            if data["parent_id"] in [None, False]:
                data["parent_id"] = None
            else:
                parent_category = CategoryGateway.get_by_id(data["parent_id"])
                if not parent_category:
                    return {
                        "errors": [error_message(LocalApiCode.invalidParentCategory)]
                    }

        category = CategoryGateway.update(category_id, **data)
        if not category:
            return {"errors": [error_message(LocalApiCode.categoryNotFound)]}

        return {"category": category.to_dict()}

    @classmethod
    def delete_category(cls, category_id):
        category = CategoryGateway.get_by_id(category_id)
        if not category:
            return {"errors": [error_message(LocalApiCode.categoryNotFound)]}

        ticketsInCategory = TicketGateway.get_by_category_id(category_id=category.id)
        if ticketsInCategory:
            return {"errors": [error_message(LocalApiCode.categoryHasTickets)]}

        subcategories = CategoryGateway.get_by_parent_id(parent_id=category.id)
        if subcategories:
            return {"errors": [error_message(LocalApiCode.categoryHasSubcategories)]}

        if category.parent_id:
            ticketsInSubcategory = TicketGateway.get_by_subcategory_id(
                subcategory_id=category.id
            )
            if ticketsInSubcategory:
                return {"errors": [error_message(LocalApiCode.subcategoryHasTickets)]}

        CategoryGateway.delete(category_id)
        return {"message": "Category deleted successfully"}
