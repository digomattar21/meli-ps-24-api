from models.severity import Severity
from .extensions import db

def seed_severities():
    severities = [
        {'level': 1, 'description': 'Issue High'},
        {'level': 2, 'description': 'High'},
        {'level': 3, 'description': 'Medium'},
        {'level': 4, 'description': 'Low'},
    ]

    existing_severities = {severity.level for severity in Severity.query.all()}

    for severity in severities:
        if severity['level'] not in existing_severities:
            new_severity = Severity(level=severity['level'], description=severity['description'])
            db.session.add(new_severity)

    db.session.commit()
