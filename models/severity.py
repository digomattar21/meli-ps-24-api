from heart.core.extensions import db


class Severity(db.Model):
    __tablename__ = "severities"

    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer, nullable=False, unique=True)
    description = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Severity {self.level} - {self.description}>"

    def to_dict(self):
        return {
            "id": self.id,
            "level": self.level,
            "description": self.description,
        }
