from models.category import Category
from heart.core.extensions import db

class CategoryGateway:

    @classmethod
    def create(cls, name, parent_id=None):
        category = Category(name=name, parent_id=parent_id)
        db.session.add(category)
        db.session.commit()
        return category

    @classmethod
    def get_by_id(cls, id):
        return Category.query.get(id)

    @classmethod
    def get_all(cls):
        return Category.query.all()

    @classmethod
    def get_by_name(cls, name):
        return Category.query.filter_by(name=name).first()

    @classmethod
    def update(cls, id, **kwargs):
        category = cls.get_by_id(id)
        if category:
            for key, value in kwargs.items():
                setattr(category, key, value)
            db.session.commit()
            return category
        return None

    @classmethod
    def delete(cls, id):
        category = cls.get_by_id(id)
        if category:
            db.session.delete(category)
            db.session.commit()
