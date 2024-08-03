from heart.core.extensions import db


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    parent_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True)
    parent = db.relationship("Category", remote_side=[id], backref="subcategories")

    def to_dict(self, include_subcategories=False):
        data = {"id": self.id, "name": self.name, "parent_id": self.parent_id}

        if include_subcategories:
            data["subcategories"] = [
                subcategory.to_dict(include_subcategories=True)
                for subcategory in self.subcategories
            ]

        return data
