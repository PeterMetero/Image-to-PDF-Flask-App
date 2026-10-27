import os
import pytest
from app import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200

def test_convert_no_images(client):
    response = client.post('/api/convert')
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data