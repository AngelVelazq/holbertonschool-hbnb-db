import pytest
from src import create_app, db
from src.models.user import User

@pytest.fixture
def app():
    app = create_app('src.config.TestingConfig')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_user_sqlalchemy(client):
    user_data = {
        'email': 'test@example.com',
        'password': 'securepassword',
        'first_name': 'John',
        'last_name': 'Doe'
    }
    response = client.post('/users/', json=user_data)
    assert response.status_code == 201
    data = response.get_json()
    assert data['email'] == user_data['email']

def test_get_user_sqlalchemy(client):
    user_data = {
        'email': 'test@example.com',
        'password': 'securepassword',
        'first_name': 'John',
        'last_name': 'Doe'
    }
    client.post('/users/', json=user_data)
    response = client.get('/users/')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['email'] == user_data['email']

def test_update_user_sqlalchemy(client):
    user_data = {
        'email': 'test@example.com',
        'password': 'securepassword',
        'first_name': 'John',
        'last_name': 'Doe'
    }
    client.post('/users/', json=user_data)
    updated_data = {
        'first_name': 'Jane'
    }
    user_id = client.get('/users/').get_json()[0]['id']
    response = client.put(f'/users/{user_id}', json=updated_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data['first_name'] == updated_data['first_name']

def test_delete_user_sqlalchemy(client):
    user_data = {
        'email': 'test@example.com',
        'password': 'securepassword',
        'first_name': 'John',
        'last_name': 'Doe'
    }
    client.post('/users/', json=user_data)
    user_id = client.get('/users/').get_json()[0]['id']
    response = client.delete(f'/users/{user_id}')
    assert response.status_code == 204
    response = client.get('/users/')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 0
