# app/gateways/ticket_gateway.py
from models.ticket import Ticket
from heart.core.extensions import db

class TicketGateway:

    @classmethod
    def create(cls, title, description, category_id, user_id, subcategory_id=None, severity_id=None):
        ticket = Ticket(
            title=title,
            description=description,
            category_id=category_id,
            subcategory_id=subcategory_id,
            severity_id=severity_id,
            user_id=user_id,
        )
        db.session.add(ticket)
        db.session.commit()
        return ticket

    @classmethod
    def get_by_id(cls, id):
        return Ticket.query.get(id)

    @classmethod
    def get_by_user_id(cls, user_id):
        return Ticket.query.filter_by(user_id=user_id).all()
    
    @classmethod
    def get_all(cls):
        return Ticket.query.all()

    @classmethod
    def update(cls, id, **kwargs):
        ticket = cls.get_by_id(id)
        if ticket:
            for key, value in kwargs.items():
                setattr(ticket, key, value)
            db.session.commit()
            return ticket
        return None

    @classmethod
    def delete(cls, id):
        ticket = cls.get_by_id(id)
        if ticket:
            db.session.delete(ticket)
            db.session.commit()
