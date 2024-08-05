from datetime import datetime, timezone

from heart.core.extensions import db


class Ticket(db.Model):
    __tablename__ = "tickets"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    subcategory_id = db.Column(
        db.Integer, db.ForeignKey("categories.id"), nullable=True
    )
    severity_id = db.Column(db.Integer, db.ForeignKey("severities.id"), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    category = db.relationship("Category", foreign_keys=[category_id])
    subcategory = db.relationship("Category", foreign_keys=[subcategory_id])
    severity = db.relationship("Severity", foreign_keys=[severity_id])

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category_id": self.category_id,
            "subcategory_id": self.subcategory_id,
            "severity_id": self.severity_id,
            "created_at": self.created_at.isoformat(),
            "category_name": self.category.name,
            "subcategory_name": self.subcategory.name if self.subcategory else None,
            "severity_level": self.severity.level if self.severity else None,
            "user_id": self.user_id,
        }

    def __repr__(self):
        return f"<Ticket {self.title}>"
