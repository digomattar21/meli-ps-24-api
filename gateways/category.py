from sqlalchemy.exc import IntegrityError

from heart.core.extensions import db
from models.category import Category


class CategoryGateway:

    @classmethod
    def create(cls, name, parent_id=None):
        category = Category(name=name, parent_id=parent_id)
        try:
            db.session.add(category)
            db.session.commit()
            return category
        except IntegrityError:
            db.session.rollback()
            return None

    @classmethod
    def get_by_id(cls, id):
        if id is None:
            return None
        return Category.query.get(id)

    @classmethod
    def get_by_parent_id(cls, parent_id):
        return Category.query.filter_by(parent_id=parent_id).all()

    @classmethod
    def get_all(cls):
        return Category.query.all()

    @classmethod
    def get_by_name(cls, name):
        return Category.query.filter_by(name=name).first()

    @classmethod
    def update(cls, id, **kwargs):
        if id is None:
            return None
        category = cls.get_by_id(id)
        if category:
            for key, value in kwargs.items():
                setattr(category, key, value)
            db.session.commit()
            return category
        return None

    @classmethod
    def delete(cls, id):
        if id is None:
            return None
        category = cls.get_by_id(id)
        if category:
            db.session.delete(category)
            db.session.commit()
