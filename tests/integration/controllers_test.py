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
    
def test_update_ticket(client):
    response = client.patch('/ticket/1', json={
        'title': 'Test Ticket 2',
        'description': 'This is a test ticket',
        'severity': 2,
        'category_id': 1,
        'subcategory_id': 7
    })
    assert response.status_code == 200
    assert response.json['ticket']['title'] == 'Test Ticket 2'

def test_get_ticket(client):
    response = client.get('/ticket')
    assert response.status_code == 200
    assert len(response.json['tickets']) > 0
    
def test_get_ticket_by_id(client):
    response = client.get('/ticket/1')
    assert response.status_code == 200
    assert response.json['ticket']

def test_delete_ticket(client):
    response = client.delete('/ticket/1')
    assert response.status_code == 200
    
def test_create_category(client):
    response = client.post('/category', json={
        "name": "Test Category",
        "parent_id": 1
    })
    assert response.status_code == 200
    category_id = response.json["category_id"]
    assert isinstance(category_id, int)


def test_get_category(client):
    response = client.get('/category')
    assert response.status_code == 200
    assert len(response.json['categories']) > 0
    
def test_get_category_by_id(client):
    response = client.get('/category/1')
    assert response.status_code == 200

def test_update_category(client):
    response = client.patch('/category/1', json={
        "name": "Teste2"
    })
    assert response.status_code == 200
    assert response.json['category']['name'] == 'Teste2'