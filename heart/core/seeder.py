from models.severity import Severity
from models.category import Category
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
    
def seed_categories():
    categories = [
        {"name": "Hardware", "parent_id": None},
        {"name": "Software", "parent_id": None},
        {"name": "Networking", "parent_id": None},
        {"name": "Security", "parent_id": None},
        {"name": "User Management", "parent_id": None},
        {"name": "Laptops", "parent_id": 1}, 
        {"name": "Desktops", "parent_id": 1}, 
        {"name": "Operating Systems", "parent_id": 2},  
        {"name": "Applications", "parent_id": 2},  
        {"name": "VPN", "parent_id": 3},  
    ]

    existing_categories = {category.name for category in Category.query.all()}

    for category in categories:
        if category['name'] not in existing_categories:
            new_category = Category(name=category['name'], parent_id=category['parent_id'])
            db.session.add(new_category)

    db.session.commit()
