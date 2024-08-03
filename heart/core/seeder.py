from models.ticket import Ticket
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

from models.ticket import Ticket
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

def seed_tickets():
    tickets = [
        {
            "title": "VPN not connecting",
            "description": "User cannot connect to the VPN.",
            "severity": 2,  
            "category_id": 1,  
            "subcategory_id": 6,  
            "user_id": 2,
        },
        {
            "title": "Software installation issue",
            "description": "Error while installing software.",
            "severity": 3, 
            "category_id": 1,  
            "subcategory_id": 6,  
            "user_id": 1,
        },
    ]

    existing_tickets = {ticket.title for ticket in Ticket.query.all()}

    for ticket in tickets:
        if ticket['title'] not in existing_tickets:
            new_ticket = Ticket(
                title=ticket['title'],
                description=ticket['description'],
                severity_id=ticket['severity'],
                category_id=ticket['category_id'],
                subcategory_id=ticket['subcategory_id'],
                user_id=ticket['user_id']
            )
            db.session.add(new_ticket)

    db.session.commit()