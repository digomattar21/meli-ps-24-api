import pytest
from app import create_app
from heart.core.extensions import db

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_create_ticket(client):
    response = client.post('/ticket', json={
        'title': 'Test Ticket',
        'description': 'This is a test ticket',
        'severity': 2,
        'category': 1,
        'subcategory': 6
    })
    assert response.status_code == 200
    assert response.json['ticket']['title'] == 'Test Ticket'
