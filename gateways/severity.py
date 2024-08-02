from models.severity import Severity
from heart.core.extensions import db

class SeverityGateway:

    @classmethod
    def create(cls, level, description):
        severity = Severity(level=level, description=description)
        db.session.add(severity)
        db.session.commit()
        return severity

    @classmethod
    def get_by_id(cls, id):
        return Severity.query.get(id)
    
    @classmethod
    def get_by_level(cls, level):
        return Severity.query.filter_by(level=level).first()

    @classmethod
    def get_all(cls):
        return Severity.query.all()

    @classmethod
    def update(cls, id, **kwargs):
        severity = cls.get_by_id(id)
        if severity:
            for key, value in kwargs.items():
                setattr(severity, key, value)
            db.session.commit()
            return severity
        return None

    @classmethod
    def delete(cls, id):
        severity = cls.get_by_id(id)
        if severity:
            db.session.delete(severity)
            db.session.commit()
